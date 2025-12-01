"""
应用配置管理
使用 Pydantic Settings 进行配置验证
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本配置
    APP_NAME: str = "AI FullStack API"
    DEBUG: bool = True
    API_PREFIX: str = "/aifs"
    
    # MongoDB 配置
    MONGO_HOST: str = "localhost"
    MONGO_PORT: int = 27017
    MONGO_USER: str = ""
    MONGO_PASSWORD: str = ""
    MONGO_DB: str = "aifs_db"
    
    @property
    def MONGO_URL(self) -> str:
        """构建 MongoDB 连接 URL"""
        if self.MONGO_USER and self.MONGO_PASSWORD:
            return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}:{self.MONGO_PORT}"
        return f"mongodb://{self.MONGO_HOST}:{self.MONGO_PORT}"
    
    # JWT 配置
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # CORS 配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()
