import asyncio
import websockets
import json
import pandas as pd
import requests

# 配置信息
BOT_TOKEN = "7828317401:AAHPa9Nc9WCs-knqW_ZtEjIzATj_ZHZ9aoU"
CHAT_ID = "6042587227"
INST_ID = "BTC-USDT"
KLINE_CHANNEL = "candle1H"

# 推送消息到Telegram
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    try:
        requests.get(url, params=params, timeout=10)
    except Exception as e:
        print(f"发送Telegram消息失败: {e}")

# 记录上一次的均线状态，避免重复推送
last_cross = None

# 处理K线数据，计算均线并判断穿越
def handle_kline(df):
    global last_cross
    df['m20'] = df['close'].rolling(window=20).mean()
    df['m60'] = df['close'].rolling(window=60).mean()
    if len(df) < 61:
        return  # 数据不足
    # 取最近两根K线，判断是否发生穿越
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    # 上穿（金叉）
    if prev['m20'] < prev['m60'] and curr['m20'] >= curr['m60']:
        if last_cross != 'golden':
            send_telegram_message(f"BTC 1小时K线出现金叉（m20上穿m60），可关注做多机会！\n当前价: {curr['close']}")
            last_cross = 'golden'
    # 下穿（死叉）
    elif prev['m20'] > prev['m60'] and curr['m20'] <= curr['m60']:
        if last_cross != 'death':
            send_telegram_message(f"BTC 1小时K线出现死叉（m20下穿m60），可关注做空机会！\n当前价: {curr['close']}")
            last_cross = 'death'

# 主协程，连接OKX WebSocket，实时获取K线
data_df = pd.DataFrame()

async def main():
    global data_df
    url = "wss://ws.okx.com:8443/ws/v5/public"
    async with websockets.connect(url) as ws:
        sub = {
            "op": "subscribe",
            "args": [{"channel": KLINE_CHANNEL, "instId": INST_ID}]
        }
        await ws.send(json.dumps(sub))
        print("已连接OKX WebSocket，开始监听K线...")
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if 'data' in data:
                k = data['data'][0]
                # k线数据格式：[ts, o, h, l, c, vol, volCcy, volCcyQuote, confirm]
                # 取出时间和收盘价
                ts = int(k[0])
                close = float(k[4])
                # 用时间戳做索引，避免重复
                data_df.loc[ts, 'close'] = close
                # 只保留最近100根K线
                data_df = data_df.sort_index().iloc[-100:]
                handle_kline(data_df)

if __name__ == "__main__":
    asyncio.run(main()) 