#!/bin/bash

# 交易所切换脚本

echo "🔄 交易所切换工具"
echo "=================="

# 显示当前配置
echo "📋 当前配置:"
python3 config.py
echo ""

# 选择交易所
echo "请选择交易所:"
echo "1) OKX (欧易)"
echo "2) Binance (币安)"
echo "3) 查看当前配置"
echo "4) 退出"
echo "=================="

read -p "请输入选择 (1-4): " choice

case $choice in
    1)
        echo "🔄 切换到OKX..."
        export EXCHANGE=OKX
        echo "✅ 已切换到OKX"
        echo ""
        echo "📋 新配置:"
        python3 config.py
        ;;
    2)
        echo "🔄 切换到Binance..."
        export EXCHANGE=Binance
        echo "✅ 已切换到Binance"
        echo ""
        echo "📋 新配置:"
        python3 config.py
        ;;
    3)
        echo "📋 当前配置:"
        python3 config.py
        ;;
    4)
        echo "👋 退出"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "💡 提示:"
echo "- 要永久保存设置，请在GitHub Actions中添加环境变量"
echo "- 或者修改config.py文件中的EXCHANGE参数"
echo "- 使用 'python3 test_monitor.py' 测试新配置"
