#!/usr/bin/env python3
"""
部署到 Render 的辅助脚本
用于检查环境和准备部署
"""

import os
import sys

def check_dependencies():
    """检查依赖包是否已安装"""
    required_packages = ['websockets', 'requests', 'pandas']
    missing_packages = []
    
    print("检查依赖包...")
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} 已安装")
        except ImportError:
            print(f"✗ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n需要安装以下包：")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\n所有依赖包已安装！")
        return True

def check_files():
    """检查必需文件是否存在"""
    required_files = ['btc_ma_alert.py', 'requirements.txt']
    missing_files = []
    
    print("\n检查必需文件...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} 存在")
        else:
            print(f"✗ {file} 不存在")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n缺少以下文件：{', '.join(missing_files)}")
        return False
    else:
        print("\n所有必需文件都存在！")
        return True

def test_telegram_connection():
    """测试 Telegram 连接"""
    try:
        import requests
        from btc_ma_alert import BOT_TOKEN, CHAT_ID
        
        print("\n测试 Telegram 连接...")
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            "chat_id": CHAT_ID,
            "text": "🚀 BTC 均线监控系统部署测试成功！"
        }
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            print("✓ Telegram 连接测试成功！")
            return True
        else:
            print(f"✗ Telegram 连接失败：{response.text}")
            return False
    except Exception as e:
        print(f"✗ Telegram 连接测试失败：{e}")
        return False

def main():
    print("=" * 50)
    print("BTC 均线监控系统 - 部署检查")
    print("=" * 50)
    
    # 检查依赖
    deps_ok = check_dependencies()
    
    # 检查文件
    files_ok = check_files()
    
    # 测试 Telegram
    telegram_ok = test_telegram_connection()
    
    print("\n" + "=" * 50)
    if deps_ok and files_ok and telegram_ok:
        print("🎉 所有检查通过！可以部署到 Render")
        print("\n下一步：")
        print("1. 把代码上传到 GitHub")
        print("2. 在 Render 创建 Background Worker")
        print("3. 配置启动命令：python btc_ma_alert.py")
    else:
        print("❌ 检查未通过，请解决上述问题后再部署")
    print("=" * 50)

if __name__ == "__main__":
    main() 