"""
依赖注入函数
用于 FastAPI 的 Depends
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pymongo.asynchronous.database import AsyncDatabase

from app.core.database import get_db
from app.core.security import decode_access_token
from app.services.user_service import get_user_by_id

# Bearer token 认证方案
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncDatabase = Depends(get_db)
) -> dict:
    """
    获取当前登录用户
    
    从请求头中提取 Bearer token，解码并验证用户
    
    Args:
        credentials: HTTP Authorization 头中的 Bearer token
        db: MongoDB 数据库实例
    
    Returns:
        当前用户字典
    
    Raises:
        HTTPException: token 无效或用户不存在
    """
    token = credentials.credentials
    
    # 解码 token
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户 ID
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查询用户
    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
