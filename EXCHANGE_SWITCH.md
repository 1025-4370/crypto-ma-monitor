# 交易所切换说明

本系统支持在OKX和Binance两个交易所之间切换，你可以根据个人偏好选择使用哪个交易所的数据。

## 支持的交易所

### 1. OKX (欧易)
- **优势**: 
  - 全球知名交易所，流动性好
  - API稳定，响应速度快
  - 支持更多交易对
  - 数据质量高
- **API地址**: `https://www.okx.com/api/v5`
- **交易对格式**: `BTC-USDT`, `ETH-USDT`

### 2. Binance (币安)
- **优势**: 
  - 全球最大交易所
  - API文档完善
  - 免费使用，无限制
  - 社区支持好
- **API地址**: `https://api.binance.com/api/v3`
- **交易对格式**: `BTCUSDT`, `ETHUSDT`

## 切换方法

### 方法一：修改配置文件

编辑 `config.py` 文件，修改 `EXCHANGE` 参数：

```python
# 使用OKX
EXCHANGE = "OKX"

# 或使用Binance
EXCHANGE = "Binance"
```

### 方法二：环境变量（推荐）

在GitHub Actions中使用环境变量，避免在代码中暴露偏好：

1. 在GitHub仓库设置中添加环境变量：
   - 进入仓库 → Settings → Secrets and variables → Actions
   - 添加变量：`EXCHANGE`，值设为 `OKX` 或 `Binance`

2. 修改 `config.py`：

```python
import os

# 从环境变量读取交易所配置，默认为OKX
EXCHANGE = os.getenv("EXCHANGE", "OKX")
```

3. 修改GitHub Actions工作流：

```yaml
- name: Run crypto monitor
  run: |
    python github_actions_monitor.py
  env:
    EXCHANGE: ${{ vars.EXCHANGE }}
    TZ: Asia/Shanghai
```

## 配置对比

| 配置项 | OKX | Binance |
|--------|-----|---------|
| 交易所名称 | `"OKX"` | `"Binance"` |
| BTC交易对 | `"BTC-USDT"` | `"BTCUSDT"` |
| ETH交易对 | `"ETH-USDT"` | `"ETHUSDT"` |
| API端点 | `/market/candles` | `/klines` |
| 数据格式 | `[ts, o, h, l, c, vol, ...]` | `[ts, o, h, l, c, vol, ...]` |
| 响应格式 | `{"code": "0", "data": [...]}` | `[...]` |

## 测试切换

### 1. 本地测试

```bash
# 测试OKX
EXCHANGE=OKX python test_monitor.py

# 测试Binance
EXCHANGE=Binance python test_monitor.py
```

### 2. 功能验证

切换后，系统会自动：
- 使用对应交易所的API
- 处理不同的数据格式
- 适配交易对命名规则
- 处理不同的错误响应

## 注意事项

### 1. API限制
- **OKX**: 免费用户每分钟1200次请求
- **Binance**: 免费用户每分钟1200次请求
- 当前配置（每15分钟检查）远低于限制

### 2. 数据差异
- 不同交易所的价格可能有微小差异
- 时间戳格式一致（毫秒级）
- K线数据格式基本相同

### 3. 网络稳定性
- OKX在全球有多个节点，访问稳定
- Binance在全球也有很好的网络覆盖
- 建议选择网络访问最稳定的交易所

### 4. 故障转移
系统设计支持在运行时切换交易所，但建议：
- 在非交易时间切换
- 先测试新配置是否正常
- 保留旧配置作为备份

## 推荐配置

### 个人使用
- **推荐**: OKX
- **原因**: 数据质量高，API稳定，支持更多交易对

### 企业使用
- **推荐**: 根据地理位置选择
- **亚洲**: OKX（网络延迟更低）
- **欧美**: Binance（网络覆盖更好）

### 开发测试
- **推荐**: 两个都配置
- **原因**: 便于对比数据，测试系统稳定性

## 故障排除

### 常见问题

1. **切换后无法获取数据**
   - 检查网络连接
   - 验证API地址是否正确
   - 确认交易对格式

2. **数据格式错误**
   - 检查配置文件中的交易对格式
   - 确认API响应格式
   - 查看错误日志

3. **推送通知异常**
   - 检查Bark配置
   - 验证网络连接
   - 查看执行日志

### 调试方法

1. **启用详细日志**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **测试API连接**
   ```bash
   curl "https://www.okx.com/api/v5/market/candles?instId=BTC-USDT&bar=15m&limit=1"
   ```

3. **检查配置文件**
   ```bash
   python -c "from config import *; print(f'Exchange: {EXCHANGE}')"
   ```

## 总结

交易所切换功能让系统更加灵活，你可以：
- 根据个人偏好选择交易所
- 在出现问题时快速切换
- 对比不同交易所的数据质量
- 适应不同的网络环境

无论选择哪个交易所，系统都会自动适配，确保功能正常运行。
