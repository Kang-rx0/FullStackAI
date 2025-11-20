# 🤖 AI全栈对话系统

> 模仿ChatGPT的AI对话平台，聚焦金融领域

## � 项目概述

**技术栈**: FastAPI + Vue3 + TypeScript + MySQL + LLM

**核心功能**:
- 用户注册/登录（JWT认证）
- 多会话管理
- AI对话（支持流式输出）
- 聊天历史持久化

## 🏗️ 系统架构

```
前端 (Vue3 + TS)  →  API层 (FastAPI)  →  业务逻辑  →  数据库 (MySQL)
                                           ↓
                                      AI模型服务
```

**分层设计**:
1. **前端层**: Vue3 + TypeScript + Element Plus
2. **API层**: FastAPI + JWT认证 + CORS
3. **业务层**: 用户服务 / 会话服务 / 聊天服务
4. **数据层**: MySQL + 连接池
5. **AI层**: OpenAI API / 本地模型

## 🛠️ 技术选型

### 后端
- **FastAPI** - 高性能异步框架
- **MySQL 8.0** - 关系型数据库
- **JWT** - 用户认证
- **bcrypt** - 密码加密

### 前端
- **Vue 3** - 前端框架
- **TypeScript** - 类型安全
- **Element Plus / Naive UI** - UI组件库
- **Pinia** - 状态管理
- **Axios** - HTTP客户端

### AI模型
- **方案A**: OpenAI API / 通义千问 / ChatGLM API
- **方案B**: 本地部署（Llama2 / ChatGLM3 / Qwen）

## 📦 功能模块 (ToDo List)

### ✅ Phase 1: 基础架构 (2周)
- [ ] 数据库设计与初始化
  - [ ] 创建users、conversations、messages表
  - [ ] 添加索引和外键约束
- [ ] 后端框架搭建
  - [ ] FastAPI项目初始化
  - [ ] 配置CORS和中间件
  - [ ] 实现JWT认证
- [ ] 前端项目初始化
  - [ ] Vue3 + TS项目创建
  - [ ] 安装UI组件库
  - [ ] 配置路由和状态管理

### � Phase 2: 用户模块 (1周)
- [ ] 用户注册功能
  - [ ] API: POST /api/v1/auth/register
  - [ ] 密码加密存储
  - [ ] 用户名唯一性验证
- [ ] 用户登录功能
  - [ ] API: POST /api/v1/auth/login
  - [ ] JWT令牌生成
  - [ ] 前端登录页面
- [ ] 用户信息管理
  - [ ] API: GET/PUT /api/v1/users/me
  - [ ] 修改密码功能

### 🔄 Phase 3: 会话模块 (1周)
- [ ] 会话列表
  - [ ] API: GET /api/v1/conversations
  - [ ] 前端会话列表组件
  - [ ] 分页加载
- [ ] 创建会话
  - [ ] API: POST /api/v1/conversations
  - [ ] 自动生成会话标题
- [ ] 删除会话
  - [ ] API: DELETE /api/v1/conversations/{id}
  - [ ] 级联删除消息
- [ ] 会话详情
  - [ ] API: GET /api/v1/conversations/{id}

### 🔄 Phase 4: 聊天模块 (2周)
- [ ] 发送消息
  - [ ] API: POST /api/v1/conversations/{id}/messages
  - [ ] 消息持久化
- [ ] AI响应生成
  - [ ] 集成OpenAI API / 本地模型
  - [ ] Prompt工程
  - [ ] 错误处理
- [ ] 消息历史
  - [ ] API: GET /api/v1/conversations/{id}/messages
  - [ ] 前端聊天界面
  - [ ] 滚动加载历史消息
- [ ] 流式响应（可选）
  - [ ] WebSocket实现
  - [ ] 打字机效果

### ⏸️ Phase 5: 优化功能 (1-2周)
- [ ] 消息操作
  - [ ] 消息编辑
  - [ ] 消息删除
  - [ ] 重新生成回答
- [ ] 会话归档
  - [ ] 归档/取消归档
  - [ ] 归档列表查询
- [ ] 搜索功能
  - [ ] 会话搜索
  - [ ] 消息搜索
- [ ] 性能优化
  - [ ] Redis缓存
  - [ ] 数据库查询优化
  - [ ] 响应缓存

### ⏸️ Phase 6: 测试与部署 (1周)
- [ ] 测试
  - [ ] 后端单元测试（pytest）
  - [ ] 前端单元测试（Vitest）
  - [ ] API集成测试
- [ ] 部署
  - [ ] Docker容器化
  - [ ] Docker Compose配置
  - [ ] Nginx配置
  - [ ] CI/CD配置

## 🗃️ 数据库设计

### 核心表结构

#### 1. users (用户表)
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 2. conversations (会话表)
```sql
CREATE TABLE conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(255) DEFAULT '新对话',
    model_name VARCHAR(50) DEFAULT 'gpt-3.5-turbo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### 3. messages (消息表)
```sql
CREATE TABLE messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    role ENUM('system', 'user', 'assistant') NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);
```

## 🔌 API接口设计

### 统一响应格式
```json
{
    "code": 200,
    "message": "success",
    "data": { ... }
}
```

### 核心接口列表

#### 认证接口
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/refresh` - 刷新令牌

#### 用户接口
- `GET /api/v1/users/me` - 获取用户信息
- `PUT /api/v1/users/me` - 更新用户信息
- `PUT /api/v1/users/me/password` - 修改密码

#### 会话接口
- `GET /api/v1/conversations` - 获取会话列表（分页）
- `POST /api/v1/conversations` - 创建新会话
- `GET /api/v1/conversations/{id}` - 获取会话详情
- `PUT /api/v1/conversations/{id}` - 更新会话
- `DELETE /api/v1/conversations/{id}` - 删除会话

#### 聊天接口
- `GET /api/v1/conversations/{id}/messages` - 获取消息历史
- `POST /api/v1/conversations/{id}/messages` - 发送消息
- `DELETE /api/v1/messages/{id}` - 删除消息
- `POST /api/v1/messages/{id}/regenerate` - 重新生成回答

**API文档**: 
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🚀 开发规范

### Git工作流
- `main`: 生产分支
- `develop`: 开发分支  
- `feature/*`: 功能开发
- `bugfix/*`: 问题修复

### 提交规范
```
feat: 新功能
fix: 修复bug
docs: 文档更新
refactor: 代码重构
test: 测试相关
```

### 代码规范
- **后端**: PEP 8, Black格式化, Flake8检查
- **前端**: ESLint + Prettier, Vue风格指南

## ⚙️ 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 后端启动

```bash
# 1. 创建虚拟环境
cd Backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 2. 安装依赖
pip install fastapi uvicorn mysql-connector-python python-jose passlib[bcrypt]

# 3. 配置.env
# 创建.env文件，配置数据库和密钥

# 4. 初始化数据库
python init_DB.py

# 5. 启动服务
uvicorn main:app --reload
# 访问: http://localhost:8000/docs
```

### 前端启动

```bash
# 1. 安装依赖
cd Frontend
npm install

# 2. 启动开发服务器
npm run dev
# 访问: http://localhost:5173
```

### Docker快速启动（可选）

```bash
# 使用Docker Compose启动全部服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 🎯 未来扩展方向

- [ ] **流式响应**: WebSocket实现打字机效果
- [ ] **多模型支持**: 允许用户切换不同AI模型
- [ ] **会话分享**: 生成会话分享链接
- [ ] **消息导出**: 导出对话历史为Markdown/PDF
- [ ] **语音输入**: 集成语音转文字功能
- [ ] **多语言支持**: i18n国际化
- [ ] **主题切换**: 明暗模式切换
- [ ] **团队协作**: 共享会话和权限管理
- [ ] **模型微调**: 金融领域LoRA微调
- [ ] **性能优化**: Redis缓存、CDN加速
- [ ] **安全加固**: 端到端加密、安全审计
- [ ] **移动端适配**: 响应式设计优化

---

## 📚 参考资料

### 官方文档
- [FastAPI](https://fastapi.tiangolo.com/)
- [Vue 3](https://vuejs.org/)
- [MySQL](https://dev.mysql.com/doc/)
- [OpenAI API](https://platform.openai.com/docs)

### 学习资源
- [FastAPI教程](https://fastapi.tiangolo.com/tutorial/)
- [Vue 3组合式API](https://vuejs.org/guide/extras/composition-api-faq.html)
- [Prompt工程指南](https://www.promptingguide.ai/)

---

## 📄 许可证

MIT License

---

## 👥 贡献指南

欢迎提交Issue和Pull Request！

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

---

**项目状态**: 🔄 开发中  
**最后更新**: 2025-11-19