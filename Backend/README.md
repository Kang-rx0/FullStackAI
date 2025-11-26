# AI FullStack Backend

基于 FastAPI + SQLAlchemy + MySQL 的后端服务。

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── api/                  # API 路由
│   │   ├── __init__.py
│   │   └── auth.py          # 认证相关接口
│   ├── core/                 # 核心配置和工具
│   │   ├── __init__.py
│   │   ├── config.py        # 应用配置
│   │   ├── database.py      # 数据库连接
│   │   └── security.py      # 安全工具（密码、JWT）
│   ├── models/               # SQLAlchemy 数据库模型
│   │   ├── __init__.py
│   │   └── user.py          # 用户模型
│   ├── schemas/              # Pydantic 数据验证模型
│   │   ├── __init__.py
│   │   └── user.py          # 用户相关 Schema
│   └── services/             # 业务逻辑层
│       ├── __init__.py
│       └── user_service.py  # 用户服务
├── .env.example              # 环境变量示例
├── requirements.txt          # 依赖列表
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
conda activate clip
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并填写实际配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置数据库密码等。

### 3. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE aifs_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 启动服务

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

服务启动后会自动创建数据库表。

### 5. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | / | API 基本信息 |
| POST | /aifs/login | 用户登录 |
| GET | /aifs/welcome | 欢迎接口 |

### 登录接口示例

**请求：**
```json
POST /aifs/login
{
  "account": "testuser",
  "password": "123456"
}
```

**响应：**
```json
{
  "message": "登录成功",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "user": {
    "id": "uuid-string",
    "username": "testuser",
    "email": null,
    "avatar_url": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
}
```

## 创建测试用户

可以使用项目根目录的 `initDB.py` 脚本或直接运行以下代码：

```python
from app.core.database import SessionLocal
from app.services.user_service import create_user

db = SessionLocal()
user = create_user(db, username="testuser", password="123456", email="test@example.com")
print(f"Created user: {user.username}")
db.close()
```
