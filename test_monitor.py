#!/usr/bin/env python3
"""
测试脚本：验证均线交叉检测和Bark推送功能
"""

import requests
import pandas as pd
from datetime import datetime
from config import *

def test_bark_notification():
    """测试Bark推送功能"""
    print("测试Bark推送功能...")
    
    title = "🧪 测试推送"
    body = f"这是一条测试消息\n时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    try:
        url = f"{BARK_URL}/{title}/{body}"
        print(f"推送URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ Bark推送测试成功！")
        else:
            print("❌ Bark推送测试失败！")
            
    except Exception as e:
        print(f"❌ Bark推送测试异常: {e}")

def test_okx_data_fetch():
    """测试OKX数据获取功能"""
    print("\n测试OKX数据获取功能...")
    
    try:
        # 测试BTC数据获取
        url = f"{OKX_API_URL}/market/candles"
        params = {
            'instId': 'BTC-USDT',
            'bar': '15m',
            'limit': 100
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get('code') == '0':
            klines = data.get('data', [])
            print(f"✅ 成功获取OKX BTC数据，共{len(klines)}条记录")
            
            # 显示最新几条数据
            if klines:
                latest = klines[-1]
                print(f"最新K线数据: 时间={latest[0]}, 收盘价={latest[4]}")
        else:
            print(f"❌ OKX API错误: {data.get('msg', '未知错误')}")
            
    except Exception as e:
        print(f"❌ OKX数据获取测试失败: {e}")

def test_binance_data_fetch():
    """测试Binance数据获取功能"""
    print("\n测试Binance数据获取功能...")
    
    try:
        # 测试BTC数据获取
        url = "https://api.binance.com/api/v3/klines"
        params = {
            'symbol': 'BTCUSDT',
            'interval': '15m',
            'limit': 100
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ 成功获取Binance BTC数据，共{len(data)}条记录")
        
        # 显示最新几条数据
        if data:
            latest = data[-1]
            print(f"最新K线数据: 时间={latest[0]}, 收盘价={latest[4]}")
            
    except Exception as e:
        print(f"❌ Binance数据获取测试失败: {e}")

def test_ma_calculation():
    """测试均线计算功能"""
    print("\n测试均线计算功能...")
    
    try:
        # 根据配置选择交易所
        if EXCHANGE.upper() == "OKX":
            print(f"使用OKX API测试...")
            url = f"{OKX_API_URL}/market/candles"
            params = {
                'instId': 'BTC-USDT',
                'bar': '15m',
                'limit': 100
            }
        else:
            print(f"使用Binance API测试...")
            url = "https://api.binance.com/api/v3/klines"
            params = {
                'symbol': 'BTCUSDT',
                'interval': '15m',
                'limit': 100
            }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # 根据交易所处理数据
        if EXCHANGE.upper() == "OKX":
            if data.get('code') != '0':
                print(f"❌ OKX API错误: {data.get('msg', '未知错误')}")
                return
            klines = data.get('data', [])
            columns = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'volCcy', 'volCcyQuote', 'confirm'
            ]
        else:
            klines = data
            columns = [
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_asset_volume', 'number_of_trades',
                'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
            ]
        
        # 转换为DataFrame
        df = pd.DataFrame(klines, columns=columns)
        df['close'] = df['close'].astype(float)
        
        # 计算均线
        df[f'm{MA_SHORT}'] = df['close'].rolling(window=MA_SHORT).mean()
        df[f'm{MA_LONG}'] = df['close'].rolling(window=MA_LONG).mean()
        
        print(f"✅ 均线计算成功")
        print(f"最新收盘价: {df['close'].iloc[-1]:.2f}")
        print(f"最新M{MA_SHORT}均线: {df[f'm{MA_SHORT}'].iloc[-1]:.2f}")
        print(f"最新M{MA_LONG}均线: {df[f'm{MA_LONG}'].iloc[-1]:.2f}")
        
        # 检查是否有交叉
        if len(df) >= 2:
            prev = df.iloc[-2]
            curr = df.iloc[-1]
            
            if not pd.isna(prev[f'm{MA_SHORT}']) and not pd.isna(prev[f'm{MA_LONG}']) and \
               not pd.isna(curr[f'm{MA_SHORT}']) and not pd.isna(curr[f'm{MA_LONG}']):
                
                if prev[f'm{MA_SHORT}'] < prev[f'm{MA_LONG}'] and curr[f'm{MA_SHORT}'] >= curr[f'm{MA_LONG}']:
                    print("🚀 检测到金叉信号！")
                elif prev[f'm{MA_SHORT}'] > prev[f'm{MA_LONG}'] and curr[f'm{MA_SHORT}'] <= curr[f'm{MA_LONG}']:
                    print("📉 检测到死叉信号！")
                else:
                    print("📊 当前无交叉信号")
        
    except Exception as e:
        print(f"❌ 均线计算测试失败: {e}")

if __name__ == "__main__":
    print("开始运行测试...")
    print(f"交易所: {EXCHANGE}")
    print(f"Bark Key: {BARK_KEY}")
    print(f"Bark URL: {BARK_URL}")
    
    # 运行测试
    test_bark_notification()
    
    if EXCHANGE.upper() == "OKX":
        test_okx_data_fetch()
    else:
        test_binance_data_fetch()
        
    test_ma_calculation()
    
    print("\n测试完成！")
