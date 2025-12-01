"""
测试登录功能
1. 先插入测试用户到 MongoDB
2. 测试登录接口
"""
import asyncio
from datetime import datetime
from pymongo import AsyncMongoClient
from passlib.context import CryptContext

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB 配置
MONGO_URL = "mongodb://localhost:27017"
MONGO_DB = "aifs"


async def create_test_user():
    """创建测试用户"""
    print("=" * 50)
    print("📝 创建测试用户")
    print("=" * 50)
    
    # 连接 MongoDB
    client = AsyncMongoClient(MONGO_URL)
    db = client[MONGO_DB]
    
    # 测试用户数据
    test_user = {
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": pwd_context.hash("123456"),  # 密码: 123456
        "avatar_url": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }
    
    # 检查用户是否已存在
    existing_user = await db.users.find_one({"username": test_user["username"]})
    
    if existing_user:
        print(f"⚠️  用户 '{test_user['username']}' 已存在")
        print(f"   ID: {existing_user['_id']}")
    else:
        # 插入测试用户
        result = await db.users.insert_one(test_user)
        print(f"✅ 创建测试用户成功!")
        print(f"   ID: {result.inserted_id}")
    
    print(f"   用户名: {test_user['username']}")
    print(f"   邮箱: {test_user['email']}")
    print(f"   密码: 123456")
    
    # 关闭连接
    await client.close()
    print()


async def list_all_users():
    """列出所有用户"""
    print("=" * 50)
    print("👥 数据库中的所有用户")
    print("=" * 50)
    
    client = AsyncMongoClient(MONGO_URL)
    db = client[MONGO_DB]
    
    users = await db.users.find().to_list(length=100)
    
    if not users:
        print("⚠️  数据库中没有用户")
    else:
        for i, user in enumerate(users, 1):
            print(f"{i}. {user['username']} ({user.get('email', 'N/A')})")
    
    await client.close()
    print()


async def test_login(username: str, password: str):
    """测试登录（模拟验证逻辑）"""
    print("=" * 50)
    print(f"🔐 测试登录: {username}")
    print("=" * 50)
    
    client = AsyncMongoClient(MONGO_URL)
    db = client[MONGO_DB]
    
    # 查找用户
    user = await db.users.find_one({"username": username})
    
    if not user:
        print(f"❌ 登录失败: 用户 '{username}' 不存在")
        await client.close()
        return False
    
    # 验证密码
    if pwd_context.verify(password, user["hashed_password"]):
        print(f"✅ 登录成功!")
        print(f"   用户ID: {user['_id']}")
        print(f"   用户名: {user['username']}")
        print(f"   邮箱: {user.get('email', 'N/A')}")
        await client.close()
        return True
    else:
        print(f"❌ 登录失败: 密码错误")
        await client.close()
        return False


async def test_api_login():
    """测试 FastAPI 登录接口"""
    print("=" * 50)
    print("🌐 测试 FastAPI 登录接口")
    print("=" * 50)
    
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/aifs/login",
                json={"account": "testuser", "password": "123456"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API 登录成功!")
                print(f"   消息: {data['message']}")
                print(f"   Token: {data['token'][:50]}...")
                print(f"   用户: {data['user']['username']}")
            else:
                print(f"❌ API 登录失败: {response.status_code}")
                print(f"   响应: {response.json()}")
    except ImportError:
        print("⚠️  需要安装 httpx: pip install httpx")
    except Exception as e:
        print(f"❌ API 请求失败: {e}")
        print("   请确保后端服务已启动: uvicorn app.main:app --reload")
    print()


async def main():
    """主函数"""
    print("\n" + "=" * 50)
    print("🧪 MongoDB + 登录功能测试")
    print("=" * 50 + "\n")
    
    # 1. 创建测试用户
    await create_test_user()
    
    # 2. 列出所有用户
    await list_all_users()
    
    # 3. 测试登录（正确密码）
    await test_login("testuser", "123456")
    print()
    
    # 4. 测试登录（错误密码）
    await test_login("testuser", "wrongpassword")
    print()
    
    # 5. 测试 API 登录（需要先启动后端服务）
    await test_api_login()
    
    print("=" * 50)
    print("🎉 测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())
