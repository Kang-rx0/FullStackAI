"""
FastAPI 应用主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.api import auth

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="AI FullStack 后端 API 服务",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI 文档
    redoc_url="/redoc",    # ReDoc 文档
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
app.include_router(auth.router, prefix=settings.API_PREFIX, tags=["认证"])


@app.on_event("startup")
async def startup_event():
    """应用启动时执行：初始化数据库"""
    print("🚀 正在初始化数据库...")
    init_db()
    print("✅ 数据库初始化完成")


@app.get("/", tags=["根路径"])
def root():
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
