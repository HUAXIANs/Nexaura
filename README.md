# NexAura - 智能图文创作助手

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/vue.js-3.x-green.svg" alt="Vue.js Version">
  <img src="https://img.shields.io/badge/FastAPI-0.x-black.svg" alt="FastAPI Version">
</p>

NexAura 是一个基于国产算力平台的智能图文创作助手，旨在帮助用户快速、高效地生成适用于小红书等社交媒体平台的精美内容。

## ✨ 功能特性

- **智能创作**：基于讯飞星火大模型，智能生成高质量的笔记标题、正文和标签。
- **多平台适配**：为小红书等平台专门优化，生成的内容风格更符合平台特性。
- **项目式管理**：用户可以创建和管理多个创作项目，方便地组织和回顾工作。
- **一键式操作**：输入一个主题，即可瞬间获得完整的图文笔记，并支持二次编辑。
- **国际化支持**：界面支持中英双语切换。

## 🛠️ 技术栈

- **后端**: Python, FastAPI, Uvicorn, PyJWT, Passlib
- **前端**: Vue.js 3, Vite, Vue Router, Vue I18n

## 📂 项目结构

```
nexaura-project/
├── nexaura-backend/
│   ├── app/
│   │   ├── routes/         # API 路由
│   │   │   ├── auth.py     # 认证 (注册, 登录)
│   │   │   ├── projects.py # 项目管理
│   │   │   └── content.py  # 内容生成
│   │   ├── main.py         # FastAPI 应用入口
│   │   └── ...
│   ├── requirements.txt    # Python 依赖
│   └── ...
├── nexaura-frontend/
│   ├── src/
│   │   ├── components/     # Vue 公共组件
│   │   ├── views/          # 页面视图
│   │   ├── locales/        # 国际化语言文件
│   │   ├── router/         # 路由配置
│   │   └── ...
│   ├── package.json        # Node.js 依赖
│   └── ...
├── README.md               # 项目说明
└── LICENSE                 # MIT 许可证
```

## 🚀 快速开始

请确保您的本地环境中已经安装了 Python (3.8+), Node.js (16+) 和 npm。

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd nexaura-project
```

### 2. 后端设置

首先，我们来启动 FastAPI 后端服务：

```bash
# 1. 进入后端目录
cd nexaura-backend

# 2. 创建并激活 Python 虚拟环境
#    - 对于 Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
#    - 对于 macOS/Linux:
#      python3 -m venv venv
#      source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行后端服务
#    注意：在某些系统上，如果遇到 PowerShell 执行策略问题，
#    可在命令前加上 Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass;
uvicorn app.main:app --reload
```
后端服务将运行在 `http://127.0.0.1:8000`。

### 3. 前端设置

接下来，在**新的终端窗口**中启动 Vue.js 前端应用：

```bash
# 1. 进入前端目录
cd nexaura-frontend

# 2. 安装依赖
npm install

# 3. 运行前端开发服务器
#    注意：在某些系统上，如果遇到 PowerShell 执行策略问题，
#    可在命令前加上 Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass;
npm run dev
```
前端应用将运行在 `http://localhost:5173` (或另一个可用端口)。现在您可以通过浏览器访问它了。

## ⚙️ 配置

### 后端环境变量

为了安全起见，建议将敏感配置信息（如 JWT 密钥）存储在环境变量中。在 `nexaura-backend/app/routes/auth.py` 中，`SECRET_KEY` 目前是硬编码的。

建议在生产环境中通过环境变量设置它，例如创建一个 `.env` 文件，并使用 `python-dotenv` 库来加载。

**.env 示例:**
```
SECRET_KEY="a_very_secure_random_string"
```

## 🔗 API 端点

以下是后端提供的主要 API 端点：

### 认证 (`/api/auth`)
- `POST /register`: 注册新用户
- `POST /login`: 用户登录，返回 JWT
- `GET /me`: 获取当前用户信息 (需要认证)

### 项目管理 (`/api/projects`)
- `POST /`: 创建新项目 (需要认证)
- `GET /`: 获取当前用户的所有项目 (需要认证)
- `GET /{project_id}`: 获取单个项目的详情 (需要认证)
- `PUT /{project_id}`: 更新项目信息 (需要认证)
- `DELETE /{project_id}`: 删除项目 (需要认证)

### 内容生成 (`/api/content`)
- `POST /generate`: 根据主题生成内容 (需要认证)
- `GET /platforms`: 获取支持的内容平台列表
- `GET /styles`: 获取支持的内容风格列表

## 🤝 贡献指南

我们欢迎各种形式的贡献！如果您想为 NexAura 做出贡献，请遵循以下步骤：

1.  **Fork** 本项目仓库。
2.  创建您的特性分支 (`git checkout -b feature/AmazingFeature`)。
3.  提交您的更改 (`git commit -m 'Add some AmazingFeature'`)。
4.  将您的分支推送到远程仓库 (`git push origin feature/AmazingFeature`)。
5.  创建一个新的 **Pull Request**。

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证。 