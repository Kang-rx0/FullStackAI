import uuid
import hashlib
from datetime import datetime


def generate_uuid():
    """
    生成唯一 UUID 字符串
    使用 UUID4 生成随机唯一标识符
    
    Returns:
        str: UUID 字符串（格式：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx）
    """
    return str(uuid.uuid4())


def hash_password(password: str) -> str:
    """对密码进行哈希处理"""
    hasher = hashlib.sha256()
    hasher.update(password.encode("utf-8"))
    return hasher.hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码和哈希是否匹配"""
    return hash_password(plain_password) == hashed_password


def get_timestamp():
    """获取当前时间戳"""
    return datetime.now()