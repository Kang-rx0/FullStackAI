"""
用户相关业务逻辑服务
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import verify_password, get_password_hash


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """通过用户名查询用户"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """通过邮箱查询用户"""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
    """通过 ID 查询用户"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_account(db: Session, account: str) -> Optional[User]:
    """
    通过账号（用户名或邮箱）查询用户
    登录时使用
    """
    # 先尝试用户名
    user = get_user_by_username(db, account)
    if user:
        return user
    # 再尝试邮箱
    return get_user_by_email(db, account)


def authenticate_user(db: Session, account: str, password: str) -> Optional[User]:
    """
    验证用户身份
    
    Args:
        db: 数据库会话
        account: 账号（用户名或邮箱）
        password: 明文密码
    
    Returns:
        验证成功返回用户对象，失败返回 None
    """
    user = get_user_by_account(db, account)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, username: str, password: str, email: Optional[str] = None) -> User:
    """
    创建新用户
    
    Args:
        db: 数据库会话
        username: 用户名
        password: 明文密码
        email: 邮箱（可选）
    
    Returns:
        新创建的用户对象
    """
    hashed_password = get_password_hash(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
