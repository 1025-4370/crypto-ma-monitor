import requests
import pandas as pd
import time
from datetime import datetime
import json
from config import *

# 记录上一次的均线状态，避免重复推送
last_cross_status = {
    'BTC': {'golden': False, 'death': False},
    'ETH': {'golden': False, 'death': False}
}

def get_okx_kline_data(symbol, interval=KLINE_INTERVAL, limit=KLINE_LIMIT):
    """获取OKX K线数据"""
    try:
        # OKX API v5 获取K线数据
        url = f"{OKX_API_URL}/market/candles"
        params = {
            'instId': symbol,
            'bar': interval,
            'limit': limit
        }
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') != '0':
            print(f"OKX API错误: {data.get('msg', '未知错误')}")
            return None
            
        klines = data.get('data', [])
        if not klines:
            print(f"未获取到{symbol}的K线数据")
            return None
        
        # OKX K线数据格式: [ts, o, h, l, c, vol, volCcy, volCcyQuote, confirm]
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'volCcy', 'volCcyQuote', 'confirm'
        ])
        
        # 转换数据类型
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(float), unit='ms')
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        
        return df
    except Exception as e:
        print(f"获取OKX {symbol}数据失败: {e}")
        return None

def get_binance_kline_data(symbol, interval=KLINE_INTERVAL, limit=KLINE_LIMIT):
    """获取Binance K线数据"""
    try:
        # 使用Binance API获取K线数据
        url = f"https://api.binance.com/api/v3/klines"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        df = pd.DataFrame(data, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
        ])
        
        # 转换数据类型
        df['timestamp'] = pd.to_datetime(df['timestamp'].astype(float), unit='ms')
        df['close'] = df['close'].astype(float)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        
        return df
    except Exception as e:
        print(f"获取Binance {symbol}数据失败: {e}")
        return None

def get_kline_data(symbol, interval=KLINE_INTERVAL, limit=KLINE_LIMIT):
    """根据配置选择交易所获取K线数据"""
    if EXCHANGE.upper() == "OKX":
        return get_okx_kline_data(symbol, interval, limit)
    else:
        return get_binance_kline_data(symbol, interval, limit)

def calculate_ma_cross(df):
    """计算均线交叉信号"""
    if len(df) < MA_LONG + 1:
        return None, None
    
    # 计算短期和长期均线
    df[f'm{MA_SHORT}'] = df['close'].rolling(window=MA_SHORT).mean()
    df[f'm{MA_LONG}'] = df['close'].rolling(window=MA_LONG).mean()
    
    # 取最近两根K线，判断是否发生穿越
    if len(df) < 2:
        return None, None
    
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    
    # 检查是否有有效数据
    if pd.isna(prev[f'm{MA_SHORT}']) or pd.isna(prev[f'm{MA_LONG}']) or \
       pd.isna(curr[f'm{MA_SHORT}']) or pd.isna(curr[f'm{MA_LONG}']):
        return None, None
    
    # 上穿（金叉）
    if prev[f'm{MA_SHORT}'] < prev[f'm{MA_LONG}'] and curr[f'm{MA_SHORT}'] >= curr[f'm{MA_LONG}']:
        return 'golden', curr['close']
    # 下穿（死叉）
    elif prev[f'm{MA_SHORT}'] > prev[f'm{MA_LONG}'] and curr[f'm{MA_SHORT}'] <= curr[f'm{MA_LONG}']:
        return 'death', curr['close']
    
    return None, None

def send_bark_notification(title, body):
    """通过Bark发送推送通知"""
    try:
        url = f"{BARK_URL}/{title}/{body}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            print(f"Bark推送成功: {title}")
        else:
            print(f"Bark推送失败: {response.status_code}")
    except Exception as e:
        print(f"Bark推送异常: {e}")

def check_ma_cross(symbol, symbol_name):
    """检查单个币种的均线交叉"""
    df = get_kline_data(symbol)
    if df is None:
        return
    
    cross_type, price = calculate_ma_cross(df)
    
    if cross_type is None:
        return
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 避免重复推送
    if cross_type == 'golden' and not last_cross_status[symbol_name]['golden']:
        title = NOTIFICATION_TITLE['golden'].format(symbol=symbol_name)
        body = NOTIFICATION_BODY['golden'].format(
            short=MA_SHORT, long=MA_LONG, price=price, time=current_time
        )
        send_bark_notification(title, body)
        last_cross_status[symbol_name]['golden'] = True
        last_cross_status[symbol_name]['death'] = False
        print(f"{symbol_name} 金叉信号已推送")
    
    elif cross_type == 'death' and not last_cross_status[symbol_name]['death']:
        title = NOTIFICATION_TITLE['death'].format(symbol=symbol_name)
        body = NOTIFICATION_BODY['death'].format(
            short=MA_SHORT, long=MA_LONG, price=price, time=current_time
        )
        send_bark_notification(title, body)
        last_cross_status[symbol_name]['death'] = True
        last_cross_status[symbol_name]['golden'] = False
        print(f"{symbol_name} 死叉信号已推送")

def main():
    """主函数"""
    print("开始监控BTC和ETH均线交叉信号...")
    print(f"交易所: {EXCHANGE}")
    print(f"Bark推送地址: {BARK_URL}")
    print(f"监控周期: {KLINE_INTERVAL}")
    print(f"均线设置: M{MA_SHORT} vs M{MA_LONG}")
    
    while True:
        try:
            # 检查所有配置的币种
            for symbol_name, symbol_code in SYMBOLS.items():
                check_ma_cross(symbol_code, symbol_name)
            
            # 等待下次检查
            print(f"检查完成，等待下次检查... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("监控已停止")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(60)  # 出错后等待1分钟再试

if __name__ == "__main__":
    main()
