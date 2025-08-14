# -*- coding: utf-8 -*-
"""
配置文件 - 加密货币均线监控系统
"""

import os

# Bark推送配置
BARK_KEY = os.getenv("BARK_KEY", "bfGAYDNaqnKbASDB9FAEgE")  # 你的Bark Key
BARK_URL = f"https://api.day.app/{BARK_KEY}"

# 交易所配置
EXCHANGE = os.getenv("EXCHANGE", "OKX").upper()  # 交易所名称：OKX 或 Binance

# OKX API配置
OKX_BASE_URL = "https://www.okx.com"
OKX_API_URL = "https://www.okx.com/api/v5"

# 监控配置
SYMBOLS = {
    'BTC': 'BTC-USDT' if EXCHANGE == "OKX" else 'BTCUSDT',
    'ETH': 'ETH-USDT' if EXCHANGE == "OKX" else 'ETHUSDT'
}

# K线配置
KLINE_INTERVAL = os.getenv("KLINE_INTERVAL", "15m")  # K线周期
KLINE_LIMIT = int(os.getenv("KLINE_LIMIT", "100"))   # 获取K线数量

# 均线配置
MA_SHORT = int(os.getenv("MA_SHORT", "20"))           # 短期均线周期
MA_LONG = int(os.getenv("MA_LONG", "60"))             # 长期均线周期

# 检查频率（秒）
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "900"))  # 15分钟 = 900秒

# 超时设置
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))  # 请求超时时间

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")      # 日志级别
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# 通知配置
NOTIFICATION_TITLE = {
    'golden': '🚀 {symbol}金叉信号',
    'death': '📉 {symbol}死叉信号'
}

NOTIFICATION_BODY = {
    'golden': '15分钟K线M{short}上穿M{long}\n当前价格: ${price:.4f}\n时间: {time}',
    'death': '15分钟K线M{short}下穿M{long}\n当前价格: ${price:.4f}\n时间: {time}'
}

# 打印配置信息
def print_config():
    """打印当前配置信息"""
    print("=" * 50)
    print("📋 当前配置信息")
    print("=" * 50)
    print(f"交易所: {EXCHANGE}")
    print(f"Bark Key: {BARK_KEY}")
    print(f"Bark URL: {BARK_URL}")
    print(f"监控周期: {KLINE_INTERVAL}")
    print(f"均线设置: M{MA_SHORT} vs M{MA_LONG}")
    print(f"检查频率: {CHECK_INTERVAL}秒")
    print(f"请求超时: {REQUEST_TIMEOUT}秒")
    print(f"监控币种: {list(SYMBOLS.keys())}")
    print(f"交易对: {list(SYMBOLS.values())}")
    print("=" * 50)

if __name__ == "__main__":
    print_config()
