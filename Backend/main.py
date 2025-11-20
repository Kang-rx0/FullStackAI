"""
FastAPI 主应用
AI 全栈对话系统后端服务
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from db import engine
from api.user import router as user_router

# 创建 FastAPI 应用实例
app = FastAPI(
    title="AI 对话系统 API",
    description="基于 FastAPI + SQLAlchemy 的 AI 对话系统后端",
    version="1.0.0"
)

# 配置 CORS（允许前端跨域访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router)


# 应用启动事件
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    print("=" * 50)
    print("🚀 AI 对话系统正在启动...")
    print("=" * 50)
    
    # 仅做基础连通性测试；若需创建表请单独运行项目根目录的 initDB.py
    if _check_db_connection():
        print("✅ 数据库连接成功！")
    else:
        print("❌ 数据库连接失败，请确认已运行 initDB.py 初始化数据库！")
    
    print("=" * 50)


def _check_db_connection() -> bool:
    """快速检查数据库连接是否可用"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        print(f"数据库检查失败: {exc}")
        return False


# 应用关闭事件
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时执行"""
    print("👋 AI 对话系统已关闭")

# ==================== 运行说明 ====================
# 使用 uvicorn 运行：
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
# 访问 API 文档：http://localhost:8000/docs
