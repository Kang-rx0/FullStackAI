"""
FastAPI 应用主入口
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import connect_db, close_db
from app.api import login, register

# 下面的生命周期函数在app = FastAPI(...)中使用，当执行到注册fastapi时会调用，并且执行到
# yield时会暂停，然后回到fastapi的正常运行，当fastapi关闭时会继续执行yield后面的代码
# 也就是注册fastapi时会启动数据库连接，然后正常的fastapi处理。等到fastapi关闭
# 例如关闭uvicorn时，会继续执行yield后面的代码，断开数据库连接
@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时连接数据库
    print("🚀 正在启动应用...")
    await connect_db()
    yield
    # 关闭时断开连接
    await close_db()
    print("👋 应用已关闭")


# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="AI FullStack 后端 API 服务",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI 文档
    redoc_url="/redoc",    # ReDoc 文档
    lifespan=lifespan,     # 生命周期管理
)

# 配置 CORS 中间件，允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],      # 允许所有 HTTP 方法
    allow_headers=["*"],      # 允许所有请求头
)

# 注册路由
# 前缀 /aifs 与前端 API 调用路径对应
app.include_router(login.router, prefix=settings.API_PREFIX, tags=["认证"])
app.include_router(register.router, prefix=settings.API_PREFIX, tags=["注册"])


@app.get("/", tags=["根路径"])
async def root():
    """根路径，返回 API 基本信息"""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "message": "API 服务正在运行"
    }


# 用于直接运行: python -m app.main
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
