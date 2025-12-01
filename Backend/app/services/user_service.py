"""
用户相关业务逻辑服务
使用 PyMongo Async API
"""
from datetime import datetime
from typing import Optional
from pymongo.asynchronous.database import AsyncDatabase
# user_helper是自定义的，用于将MongoDB的文档格式转换为标准的用户字典格式
from app.models.user import user_helper
from app.core.security import verify_password, get_password_hash


async def get_user_by_username(db: AsyncDatabase, username: str) -> Optional[dict]:
    """通过用户名查询用户"""
    user = await db.users.find_one({"username": username})
    if user:
        # 如果查询到了，用user_helper将 MongoDB 文档转换为标准格式后返回
        return user_helper(user)
    return None


async def get_user_by_email(db: AsyncDatabase, email: str) -> Optional[dict]:
    """通过邮箱查询用户"""
    user = await db.users.find_one({"email": email})
    if user:
        return user_helper(user)
    return None


async def get_user_by_id(db: AsyncDatabase, user_id: str) -> Optional[dict]:
    """通过 ID 查询用户"""
    from bson import ObjectId
    try:
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return user_helper(user)
    except:
        pass
    return None


async def get_user_by_account(db: AsyncDatabase, account: str) -> Optional[dict]:
    """
    通过账号（用户名或邮箱）查询用户
    登录时使用
    """
    # 先尝试用户名
    user = await get_user_by_username(db, account)
    if user:
        return user
    # 再尝试邮箱
    return await get_user_by_email(db, account)


async def authenticate_user(db: AsyncDatabase, account: str, password: str) -> Optional[dict]:
    """
    验证用户身份
    
    Args:
        db: MongoDB 数据库实例
        account: 账号（用户名或邮箱）
        password: 明文密码
    
    Returns:
        验证成功返回用户字典，失败返回 None
    """
    user = await get_user_by_account(db, account)
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return user


async def create_user(db: AsyncDatabase, username: str, password: str, email: Optional[str] = None) -> dict:
    """
    创建新用户
    
    Args:
        db: MongoDB 数据库实例
        username: 用户名
        password: 明文密码
        email: 邮箱（可选）
    
    Returns:
        新创建的用户字典
    """
    hashed_password = get_password_hash(password)
    now = datetime.utcnow()
    
    user_doc = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "avatar_url": None,
        "created_at": now,
        "updated_at": now,
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    return user_helper(user_doc)
