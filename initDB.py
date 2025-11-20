"""项目初始化脚本，用于创建数据库 schema 并同步所有表结构。"""

from __future__ import annotations

import os
import sys
from typing import Final

import pymysql
from sqlalchemy import text

# 确保能够导入 Backend 目录下的模块
PROJECT_ROOT = os.path.dirname(__file__)
BACKEND_DIR = os.path.join(PROJECT_ROOT, "Backend")
if BACKEND_DIR not in sys.path:
    sys.path.append(BACKEND_DIR)

from db import engine, Base 
from model import conversation, message, user   # 注册模型到 Base.metadata

DB_NAME: Final[str] = "aifs"
DB_USER: Final[str] = "root"
DB_PASSWORD: Final[str] = "0406"
DB_HOST: Final[str] = "localhost"
DB_PORT: Final[int] = 3306


def create_database_if_not_exists() -> bool:
    """创建数据库（如果不存在）。"""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        connection.close()
        print(f"✅ 数据库 '{DB_NAME}' 已创建/已存在")
        return True
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ 创建数据库失败: {exc}")
        return False


def test_connection() -> bool:
    """快速验证 SQLAlchemy 引擎是否可以连接到数据库。"""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ SQLAlchemy 连接测试通过")
        return True
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ SQLAlchemy 连接测试失败: {exc}")
        return False


def create_tables() -> None:
    """根据 SQLAlchemy 模型创建所有表。"""
    Base.metadata.create_all(bind=engine)
    print("✅ 所有表结构已同步")


def main() -> None:
    """入口函数：先建库，再建表。"""
    print("=" * 60)
    print("🚀 正在初始化数据库...")
    print("=" * 60)

    if not create_database_if_not_exists():
        return

    if not test_connection():
        print("❌ 无法连接数据库，请确认账号/密码/端口配置！")
        return

    create_tables()
    print("=" * 60)
    print("🎉 数据库初始化完成！")
    print("提示：若需要重新生成表结构，可再次运行本脚本。")
    print("=" * 60)


if __name__ == "__main__":
    main()
