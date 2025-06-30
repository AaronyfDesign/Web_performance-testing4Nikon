# 🏮 尼康官网自动化性能测试套件

## 📋 项目概述

本项目是一个针对尼康官网 (https://my.nikon.com.cn) 的自动化性能测试套件，使用 Python + Selenium + Lighthouse 技术栈，提供全面的性能评估和交互响应测试。

### 🎯 主要功能

- **页面性能测试**: 使用 Lighthouse 评估核心页面性能
- **交互响应测试**: 测试用户操作的响应时间
- **可视化报告**: 生成详细的 HTML 测试报告
- **风险控制**: 严格限制测试频率，避免对服务器造成负担

### 🚀 快速开始

#### 1. 环境准备
```bash
# 确保已安装以下软件
- Python 3.8+
- Node.js 14+
- Chrome 浏览器

# 克隆项目
git clone <repository-url>
cd web_performance
```

#### 2. 一键启动测试
```bash
# 运行启动脚本（会自动检查和安装依赖）
python run_test.py

# 或者手动安装依赖后运行
pip install -r requirements.txt
npm install -g lighthouse
python nikon_performance_test.py
```

#### 3. 查看测试结果
测试完成后会生成以下文件：
- `nikon_performance_report_YYYYMMDD_HHMMSS.html` - 可视化测试报告
- `nikon_performance_data_YYYYMMDD_HHMMSS.csv` - 页面性能数据
- `nikon_interaction_data_YYYYMMDD_HHMMSS.csv` - 交互响应数据

## 📊 测试内容

### 页面性能测试
- 🏠 首页性能评估
- 📷 照片页面加载速度
- 📚 学习讨论页面性能
- 👥 摄影圈社区功能
- 🖼️ 直营店画廊展示

### 交互响应测试
- ⚡ 页面跳转响应时间
- 👍 帖子点赞功能测试
- 💬 评论发布响应测试（会在终端显示评论的帖子链接）
- 🔐 用户登录性能

### 性能评级标准
- **优秀**: 响应时间 ≤ 200ms, Lighthouse评分 ≥ 90
- **良好**: 响应时间 ≤ 500ms, Lighthouse评分 50-89
- **可接受**: 响应时间 ≤ 1000ms
- **差**: 响应时间 > 1000ms, Lighthouse评分 < 50

## 🔧 配置说明

### 测试账号配置
脚本中已配置测试账号信息（使用手机号密码登录）：
```python
TEST_USER = {
    "phone": "18727560912",
    "password": "Nk123456"
}
```

### 测试限制设置
- 最多测试 3 个帖子
- 每个帖子最多 1 次点赞
- 最多发布 2 条评论
- 评论内容: ["赞", "好看"]
- 操作间隔: 5 秒
- **评论时会在终端打印帖子链接**

## 📈 测试过程示例

### 交互测试输出
```
📝 正在对帖子发表评论
📱 评论帖子链接: https://my.nikon.com.cn/post/detail/626721
💬 评论内容: 赞
✅ 评论响应时间: 450ms (内容: 赞)
```

### 关键指标说明
- **FCP (First Contentful Paint)**: 首次内容绘制时间
- **LCP (Largest Contentful Paint)**: 最大内容绘制时间
- **CLS (Cumulative Layout Shift)**: 累计布局偏移
- **Speed Index**: 速度指数

## 🛡️ 安全与风险控制

### 测试约束
- ✅ 仅进行性能测试，不涉及功能破坏
- ✅ 严格控制评论数量（≤ 2 条）
- ✅ 增加操作间隔，避免频繁请求
- ✅ 使用指定测试账号，不影响真实用户
- ✅ 登录方式：手机号 + 密码

### 数据保护
- 测试数据仅本地存储
- 不收集用户个人信息
- 遵循网站使用条款
- 评论操作会在终端明确显示目标链接

## 📁 项目结构

```
web_performance/
├── nikon_performance_test.py    # 主测试脚本
├── run_test.py                  # 启动脚本
├── requirements.txt             # Python依赖
├── 测试方案文档.md               # 详细测试方案
├── README.md                    # 项目说明
└── reports/                     # 测试报告目录
    ├── *.html                   # HTML报告
    └── *.csv                    # 数据文件
```

## 🤔 常见问题

### Q: Lighthouse 安装失败？
A: 确保 Node.js 版本 ≥ 14，然后运行：
```bash
npm install -g lighthouse
```

### Q: Chrome 驱动问题？
A: 脚本会自动管理 Chrome 驱动，确保 Chrome 浏览器已安装。

### Q: 测试超时？
A: 检查网络连接，可以适当增加等待时间。

### Q: 登录失败？
A: 验证测试账号信息是否正确，确保账号未被锁定。账号使用手机号 + 密码登录方式。

## 🔄 更新日志

### v1.0.1 (2024-06-27)
- 🔧 优化评论操作，明确在终端显示帖子链接
- 📱 确认使用手机号密码登录方式
- 📝 改进交互测试的输出信息

### v1.0.0 (2024-06-27)
- ✨ 首次发布
- 🚀 支持页面性能和交互响应测试
- 📊 生成详细的HTML可视化报告
- 🛡️ 完善的风险控制机制

## 📞 技术支持

如遇问题，请查看：
1. 📋 [测试方案文档.md](测试方案文档.md) - 详细技术说明
2. 🐛 [Issues](https://github.com/your-repo/issues) - 问题反馈
3. 📧 联系开发者

## 📄 许可证

本项目仅用于性能测试目的，请遵守相关网站的使用条款。

---

**⚠️ 重要提醒**: 本测试工具仅用于性能评估，请勿用于任何破坏性测试或违规操作。测试过程中会在终端明确打印评论的帖子URL以便跟踪和监控。
