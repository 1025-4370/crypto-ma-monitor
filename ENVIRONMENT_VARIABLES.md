# 环境变量配置说明

本系统支持通过环境变量进行配置，这样可以更灵活地管理配置，特别是在GitHub Actions等CI/CD环境中。

## 支持的环境变量

### 基础配置

| 变量名 | 默认值 | 说明 | 示例 |
|--------|--------|------|------|
| `EXCHANGE` | `OKX` | 交易所选择 | `OKX` 或 `Binance` |
| `BARK_KEY` | `bfGAYDNaqnKbASDB9FAEgE` | Bark推送密钥 | 你的实际Bark Key |

### 技术参数

| 变量名 | 默认值 | 说明 | 示例 |
|--------|--------|------|------|
| `KLINE_INTERVAL` | `15m` | K线周期 | `1m`, `5m`, `15m`, `1h` |
| `KLINE_LIMIT` | `100` | 获取K线数量 | `50`, `100`, `200` |
| `MA_SHORT` | `20` | 短期均线周期 | `10`, `20`, `30` |
| `MA_LONG` | `60` | 长期均线周期 | `50`, `60`, `100` |
| `CHECK_INTERVAL` | `900` | 检查频率（秒） | `300`(5分钟), `900`(15分钟) |
| `REQUEST_TIMEOUT` | `10` | 请求超时时间（秒） | `5`, `10`, `15` |

### 日志配置

| 变量名 | 默认值 | 说明 | 示例 |
|--------|--------|------|------|
| `LOG_LEVEL` | `INFO` | 日志级别 | `DEBUG`, `INFO`, `WARNING` |

## 配置方法

### 1. 本地环境变量

#### Linux/macOS
```bash
# 设置环境变量
export EXCHANGE=Binance
export BARK_KEY=your_bark_key_here
export KLINE_INTERVAL=5m

# 运行脚本
python3 crypto_ma_monitor.py
```

#### Windows (CMD)
```cmd
set EXCHANGE=Binance
set BARK_KEY=your_bark_key_here
python crypto_ma_monitor.py
```

#### Windows (PowerShell)
```powershell
$env:EXCHANGE="Binance"
$env:BARK_KEY="your_bark_key_here"
python crypto_ma_monitor.py
```

### 2. 一次性设置

```bash
# 使用环境变量运行
EXCHANGE=Binance BARK_KEY=your_key python3 crypto_ma_monitor.py

# 或者
EXCHANGE=Binance python3 crypto_ma_monitor.py
```

### 3. 环境变量文件 (.env)

创建 `.env` 文件：
```bash
# .env
EXCHANGE=OKX
BARK_KEY=your_bark_key_here
KLINE_INTERVAL=15m
MA_SHORT=20
MA_LONG=60
```

然后使用 `python-dotenv` 加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

## GitHub Actions 配置

### 1. 添加环境变量

在GitHub仓库中：
1. 进入仓库 → Settings → Secrets and variables → Actions
2. 点击 "Variables" 标签
3. 点击 "New repository variable"
4. 添加变量

### 2. 推荐的环境变量

#### 公开变量 (Variables)
- `EXCHANGE`: 交易所选择
- `KLINE_INTERVAL`: K线周期
- `MA_SHORT`: 短期均线
- `MA_LONG`: 长期均线

#### 私密变量 (Secrets)
- `BARK_KEY`: Bark推送密钥

### 3. 工作流配置

```yaml
- name: Run crypto monitor
  run: |
    python github_actions_monitor.py
  env:
    EXCHANGE: ${{ vars.EXCHANGE || 'OKX' }}
    BARK_KEY: ${{ secrets.BARK_KEY || 'default_key' }}
    KLINE_INTERVAL: ${{ vars.KLINE_INTERVAL || '15m' }}
    MA_SHORT: ${{ vars.MA_SHORT || '20' }}
    MA_LONG: ${{ vars.MA_LONG || '60' }}
```

## 配置优先级

环境变量的优先级从高到低：

1. **环境变量** (最高优先级)
2. **配置文件默认值** (最低优先级)

例如：
```bash
# 如果设置了环境变量
export MA_SHORT=10

# 即使config.py中设置MA_SHORT=20
# 实际使用的值仍然是10
```

## 常用配置组合

### 快速监控配置
```bash
export KLINE_INTERVAL=5m
export CHECK_INTERVAL=300
export MA_SHORT=10
export MA_LONG=30
```

### 长期趋势配置
```bash
export KLINE_INTERVAL=1h
export CHECK_INTERVAL=3600
export MA_SHORT=50
export MA_LONG=200
```

### 高频交易配置
```bash
export KLINE_INTERVAL=1m
export CHECK_INTERVAL=60
export MA_SHORT=5
export MA_LONG=20
```

## 验证配置

### 1. 查看当前配置
```bash
python3 config.py
```

### 2. 测试配置
```bash
# 测试OKX
EXCHANGE=OKX python3 test_monitor.py

# 测试Binance
EXCHANGE=Binance python3 test_monitor.py
```

### 3. 检查环境变量
```bash
# Linux/macOS
env | grep -E "(EXCHANGE|BARK_KEY|KLINE)"

# Windows
set | findstr /i "EXCHANGE BARK_KEY KLINE"
```

## 故障排除

### 常见问题

1. **环境变量不生效**
   - 检查变量名是否正确
   - 确认变量值没有引号
   - 重启终端或重新加载环境

2. **配置冲突**
   - 检查环境变量和配置文件
   - 使用 `python3 config.py` 查看实际配置
   - 清除冲突的环境变量

3. **GitHub Actions 变量不工作**
   - 确认变量类型 (Variables vs Secrets)
   - 检查工作流语法
   - 查看Actions日志

### 调试技巧

1. **启用调试日志**
   ```bash
   export LOG_LEVEL=DEBUG
   python3 crypto_ma_monitor.py
   ```

2. **检查配置加载**
   ```bash
   python3 -c "from config import *; print(f'Exchange: {EXCHANGE}')"
   ```

3. **测试API连接**
   ```bash
   # 测试OKX
   curl "https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=15m&limit=1"
   
   # 测试Binance
   curl "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=1"
   ```

## 最佳实践

1. **敏感信息使用Secrets**
   - Bark Key等敏感信息使用GitHub Secrets
   - 不要在代码中硬编码

2. **配置分层管理**
   - 默认值放在config.py
   - 环境特定配置使用环境变量
   - 个人配置使用本地环境变量

3. **配置验证**
   - 部署前验证配置
   - 使用测试脚本验证
   - 监控配置变化

4. **文档化配置**
   - 记录所有环境变量
   - 说明配置的用途
   - 提供配置示例

通过环境变量配置，你可以更灵活地管理不同环境的设置，而无需修改代码。
