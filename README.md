# 抖音视频监控工具

> 基于 Playwright 的抖音视频数据采集与监控工具

## 📖 项目简介

在做短视频数据分析时，需要定期获取抖音视频的公开数据（标题、点赞数、评论数等）。手动采集效率低且容易遗漏，因此开发了这个自动化监控工具。

本项目使用 Playwright 模拟浏览器行为，能够处理抖音页面的动态加载内容，并将采集到的数据保存到本地，方便后续分析。

## ✨ 功能特性

- 🔍 自动访问指定抖音视频页面
- 📊 提取视频标题、点赞数、评论数、发布时间等公开数据
- 💾 数据保存为 JSON / CSV 格式
- ⏰ 支持定时监控，检测数据变化
- 🐳 提供 Docker 部署方案
- ✅ 包含完整的测试用例

## 🛠️ 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.11 |
| 浏览器自动化 | Playwright 1.62 |
| 测试框架 | Pytest + pytest-asyncio |
| 环境管理 | python-dotenv |
| 网络请求 | Requests |
| 容器化 | Docker + Docker Compose |

## 📁 项目结构
douyin-monitor/
├── src/ # 源代码
├── data/ # 数据存储目录
├── logs/ # 日志目录
├── main.py # 主入口
├── test_browser.py # 浏览器测试
├── test_db.py # 数据库测试
├── test_douyin.py # 抖音采集测试
├── test_phase1.py # 阶段测试
├── test_douyin_page.png # 运行截图
├── docker-compose.yml # Docker 编排配置
├── Dockerfile # Docker 镜像配置
├── requirements.txt # 依赖列表
├── .env.example # 环境变量示例
├── .gitignore # Git 忽略规则
└── README.md # 项目说明


## 🚀 快速开始

### 环境要求

- Python 3.10+
- Windows / macOS / Linux
- （可选）Docker

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/xieyn9988/douyin-monitor.git
cd douyin-monitor

# 2. 创建虚拟环境
python -m venv venv

# Windows 激活
venv\Scripts\activate

# macOS/Linux 激活
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 安装 Playwright 浏览器
playwright install chromium

# 5. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的配置

# 6. 运行
python main.py

使用 Docker 运行
docker-compose up -d

使用示例
from src.scraper import DouyinMonitor

monitor = DouyinMonitor()
result = monitor.check("https://www.douyin.com/video/xxxxx")
print(result)

运行测试
pytest test_*.py -v

运行截图
<img width="1280" height="720" alt="test_douyin_page" src="https://github.com/user-attachments/assets/6e94c29a-3f1f-48e6-9e4e-62dd09d2770a" />


⚠️ 免责声明
本项目仅供学习研究使用

请遵守抖音用户协议和 Robots 协议

禁止用于商业用途或大规模数据采集

使用前请自行评估法律风险


📈 后续计划
□ 支持多视频批量监控
□ 添加数据可视化面板
□ 支持导出 Excel 报告
□ 增加更多反爬策略
👤 作者
谢鹰

求职方向：Python 开发 / 数据分析

GitHub: @xieying

邮箱: 420309519@qq.com

⭐ 如果这个项目对你有帮助，欢迎 Star！
