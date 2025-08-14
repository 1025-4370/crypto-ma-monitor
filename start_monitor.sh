#!/bin/bash

# 加密货币均线监控系统启动脚本

echo "🚀 启动加密货币均线交叉监控系统..."
echo "=================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查依赖是否安装
echo "📦 检查依赖包..."
if ! python3 -c "import requests, pandas" 2>/dev/null; then
    echo "📥 安装依赖包..."
    pip3 install -r requirements.txt
fi

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "❌ 错误: 未找到config.py配置文件"
    exit 1
fi

echo "✅ 环境检查完成"
echo "=================================="
echo "选择运行模式:"
echo "1) 本地持续监控模式"
echo "2) 单次检查模式（用于测试）"
echo "3) 测试Bark推送"
echo "=================================="

read -p "请输入选择 (1-3): " choice

case $choice in
    1)
        echo "🔄 启动持续监控模式..."
        python3 crypto_ma_monitor.py
        ;;
    2)
        echo "🔍 运行单次检查..."
        python3 github_actions_monitor.py
        ;;
    3)
        echo "🧪 测试Bark推送..."
        python3 test_monitor.py
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac
