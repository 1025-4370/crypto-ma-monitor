# BTC 均线监控信号系统

## 功能说明
- 实时监控 BTC-USDT 1小时K线
- 计算 m20 和 m60 均线
- 检测 m20 上穿/下穿 m60 时推送 Telegram 信号

## 部署到 Render 步骤

### 1. 上传代码到 GitHub
1. 注册并登录 [GitHub](https://github.com/)
2. 新建仓库（如：btc-ma-alert）
3. 上传以下文件到仓库：
   - `btc_ma_alert.py` (主程序)
   - `requirements.txt` (依赖包列表)

### 2. 在 Render 创建后台服务
1. 登录 [dashboard.render.com](https://dashboard.render.com/)
2. 点击 "New +" → 选择 "Background Worker"
3. 连接 GitHub 账号并选择你的仓库
4. 填写配置：
   - **Service Name**: btc-ma-alert (随意)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python btc_ma_alert.py`
5. 点击 "Create Background Worker"

### 3. 等待部署完成
- Render 会自动安装依赖并启动脚本
- 服务状态显示 "Running" 表示部署成功
- 可以在日志中查看运行状态

### 4. 管理服务
- 在 Render 控制台可以随时 Start/Stop/Restart 服务
- 每次更新 GitHub 代码，Render 会自动重新部署

## 注意事项
- 确保 Telegram Bot Token 和 Chat ID 正确配置
- 服务会 24 小时运行，直到手动停止或超出免费额度
- 免费版每月 750 小时，足够全天候运行一个月 