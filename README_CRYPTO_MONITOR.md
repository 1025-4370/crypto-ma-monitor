# 加密货币均线交叉监控系统

这是一个自动监控BTC和ETH数字货币均线交叉信号的系统，当M20均线交叉M60均线时，通过Bark推送通知到手机。

## 功能特性

- 🚀 监控BTC和ETH的15分钟K线数据
- 📊 自动计算M20和M60移动平均线
- 🔔 检测金叉（M20上穿M60）和死叉（M20下穿M60）信号
- 📱 通过Bark推送通知到手机
- ⏰ 每15分钟自动检查一次
- 🔄 避免重复推送相同信号

## 系统架构

```
GitHub Actions (每15分钟运行)
    ↓
获取Binance API数据 (15分钟K线)
    ↓
计算M20和M60均线
    ↓
检测交叉信号
    ↓
Bark推送通知
```

## 安装和配置

### 1. 克隆代码库

```bash
git clone <your-repo-url>
cd btc-monitor
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置Bark推送

在 `crypto_ma_monitor.py` 中修改你的Bark Key：

```python
BARK_KEY = "你的Bark Key"  # 替换为你的实际Key
```

### 4. 测试功能

运行测试脚本验证配置：

```bash
python test_monitor.py
```

## 使用方法

### 本地运行

```bash
python crypto_ma_monitor.py
```

### GitHub Actions自动运行

系统已配置GitHub Actions工作流，每15分钟自动运行一次：

1. 将代码推送到GitHub
2. 在仓库的Actions页面查看运行状态
3. 系统会自动监控并推送信号

## 信号说明

### 金叉信号 🚀
- **触发条件**: M20均线上穿M60均线
- **技术含义**: 短期趋势转强，可能上涨
- **推送内容**: 包含当前价格和时间信息

### 死叉信号 📉
- **触发条件**: M20均线下穿M60均线
- **技术含义**: 短期趋势转弱，可能下跌
- **推送内容**: 包含当前价格和时间信息

## 配置参数

### 监控参数
- **K线周期**: 15分钟
- **均线周期**: M20, M60
- **检查频率**: 每15分钟
- **数据源**: Binance API

### 推送配置
- **推送服务**: Bark
- **推送频率**: 仅在信号触发时
- **防重复**: 避免重复推送相同信号

## 文件说明

- `crypto_ma_monitor.py` - 主监控脚本
- `test_monitor.py` - 测试脚本
- `.github/workflows/crypto_monitor.yml` - GitHub Actions工作流
- `requirements.txt` - Python依赖包
- `README_CRYPTO_MONITOR.md` - 本说明文档

## 注意事项

1. **API限制**: Binance API有访问频率限制，当前配置符合要求
2. **网络稳定性**: 确保GitHub Actions能正常访问Binance API
3. **时区设置**: 系统使用UTC时间，推送时间会显示为北京时间+8小时
4. **信号延迟**: 由于是15分钟K线，信号会有一定延迟

## 故障排除

### 常见问题

1. **Bark推送失败**
   - 检查Bark Key是否正确
   - 确认网络连接正常

2. **数据获取失败**
   - 检查Binance API是否可访问
   - 确认网络连接稳定

3. **GitHub Actions运行失败**
   - 检查工作流文件语法
   - 查看Actions日志获取详细错误信息

### 日志查看

在GitHub Actions中查看运行日志，了解每次执行的详细情况。

## 更新和维护

- 定期检查Binance API的稳定性
- 根据需要调整均线周期参数
- 监控GitHub Actions的运行状态

## 技术支持

如有问题，请检查：
1. 代码配置是否正确
2. 网络连接是否正常
3. GitHub Actions是否正常运行
4. Bark推送是否配置正确

---

**免责声明**: 本系统仅用于技术分析参考，不构成投资建议。投资有风险，入市需谨慎。
