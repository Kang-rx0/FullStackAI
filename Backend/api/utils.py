"""User API 辅助函数"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from model.user import User
from utils import hash_password, verify_password

def ensure_unique_user(db: Session, username: str, email: str | None = None) -> None:
    """检查用户名和邮箱是否已存在"""
    if db.query(User).filter(User.username == username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    if email:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被使用"
            )


def create_user_model(
    username: str,
    password: str,
    email: str | None = None,
    avatar_url: str | None = None,
) -> User:
    """根据表单数据构建 User ORM 实例"""
    return User(
        username=username,
        password_hash=hash_password(password),
        email=email,
        avatar_url=avatar_url,
    )


def authenticate_user(db: Session, username: str, password: str) -> User:
    """根据用户名和密码验证用户"""
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    return user


def serialize_user(user: User) -> dict:
    """将用户模型转换为对外响应"""
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
