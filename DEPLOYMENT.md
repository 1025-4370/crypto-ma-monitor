# 部署说明 - 加密货币均线监控系统

## 快速部署到GitHub

### 1. 准备工作

确保你已经：
- 安装了Git
- 有GitHub账号
- 安装了Python 3.7+

### 2. 创建GitHub仓库

1. 在GitHub上创建一个新的仓库
2. 仓库名称建议：`crypto-ma-monitor` 或 `btc-eth-monitor`
3. 选择Public（公开）仓库（免费用户只能使用公开仓库运行GitHub Actions）

### 3. 上传代码到GitHub

```bash
# 进入项目目录
cd btc-monitor

# 初始化Git仓库（如果还没有初始化）
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 加密货币均线监控系统"

# 添加远程仓库（替换为你的GitHub仓库URL）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送到GitHub
git push -u origin main
```

### 4. 配置Bark推送

1. 在手机上安装Bark应用
2. 获取你的Bark Key
3. 编辑 `config.py` 文件，修改 `BARK_KEY` 为你的实际Key：

```python
BARK_KEY = "你的Bark Key"  # 替换这里
```

4. 提交并推送更改：

```bash
git add config.py
git commit -m "Update Bark key"
git push
```

### 5. 启用GitHub Actions

1. 在GitHub仓库页面，点击 "Actions" 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 系统会自动检测到 `.github/workflows/crypto_monitor.yml` 文件
4. 在Actions页面可以看到工作流已经启用

### 6. 测试系统

#### 手动测试
1. 在Actions页面，找到 "Crypto MA Monitor" 工作流
2. 点击 "Run workflow" 按钮
3. 选择 "main" 分支，点击 "Run workflow"
4. 等待执行完成，查看日志

#### 查看日志
1. 点击运行中的工作流
2. 点击 "monitor" 任务
3. 查看详细执行日志

### 7. 验证推送

如果一切正常，你应该能在手机上收到Bark推送通知。

## 配置说明

### 修改监控参数

编辑 `config.py` 文件：

```python
# 修改均线周期
MA_SHORT = 20    # 短期均线
MA_LONG = 60     # 长期均线

# 修改K线周期
KLINE_INTERVAL = '15m'  # 可选: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M

# 修改检查频率（秒）
CHECK_INTERVAL = 900  # 15分钟
```

### 添加更多币种

在 `config.py` 中添加：

```python
SYMBOLS = {
    'BTC': 'BTCUSDT',
    'ETH': 'ETHUSDT',
    'BNB': 'BNBUSDT',  # 添加BNB
    'ADA': 'ADAUSDT',  # 添加ADA
}
```

## 故障排除

### 常见问题

1. **GitHub Actions不运行**
   - 检查仓库是否为公开仓库
   - 确认 `.github/workflows/` 目录存在
   - 检查YAML文件语法是否正确

2. **Bark推送失败**
   - 确认Bark Key正确
   - 检查网络连接
   - 查看Actions日志中的错误信息

3. **数据获取失败**
   - 检查Binance API是否可访问
   - 确认网络连接稳定
   - 查看错误日志

### 查看日志

在GitHub Actions中：
1. 点击失败的工作流
2. 查看具体错误信息
3. 根据错误信息进行修复

## 维护和更新

### 定期检查

1. 监控GitHub Actions运行状态
2. 检查Bark推送是否正常
3. 关注Binance API的变化

### 更新代码

```bash
# 拉取最新代码
git pull origin main

# 修改代码后
git add .
git commit -m "Update: 描述你的更改"
git push origin main
```

### 备份配置

建议备份你的 `config.py` 文件，特别是Bark Key等敏感信息。

## 安全注意事项

1. **不要将Bark Key提交到公开仓库**
   - 考虑使用GitHub Secrets存储敏感信息
   - 或者使用环境变量

2. **API限制**
   - Binance API有访问频率限制
   - 当前配置符合免费用户限制

3. **监控日志**
   - 定期检查GitHub Actions日志
   - 关注异常情况

## 联系支持

如果遇到问题：
1. 检查GitHub Actions日志
2. 查看本项目的Issues页面
3. 确认配置是否正确

---

**注意**: 本系统仅用于技术分析参考，不构成投资建议。投资有风险，入市需谨慎。
