import sys
import os

# 目录域配置
DIRECTORY_DOMAIN = "local"

# 要禁用的用户列表（用户名/手机号）
USERS_TO_DISABLE = [
    "13800138000",  # 李思
    "17775163822",  # 刘欣
    "19951332808",  # 罗勇
    "15973644283",  # 徐宇
    "13381306192",  # 朱萱
    "13861412424",  # 马磊
]


def disable_user_v1(username: str) -> dict:
    """
    禁用用户 - v1 API
    接口：/api/v1/localUser/updateUserByName
    将 status 设置为 0（禁用）
    """
    path = "/api/v1/localUser/updateUserByName"
    
    body = {
        "name": username,
        "status": 0,  # 0=禁用，1=启用
    }
    
    res = public.post(path, body)
    print(f"请求体：{body}")
    if res.status_code == 200 and res.json().get("code") == 0:
        print(f"[OK] 用户 {username} 已禁用")
        return res.json()
    else:
        print(f"[FAIL] 用户 {username} 禁用失败：{res.json()}")
        return None


def disable_user_v3(username: str) -> dict:
    """
    禁用用户 - v3 API
    接口：/api/v3/user/updateByName
    """
    path = "/api/v3/user/updateByName"
    
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "name": username,
        "status": 0,  # 0=禁用，1=启用
    }
    
    res = public.post(path, body=body, query={"lang": "zh-CN"})
    print(f"请求体：{body}")
    if res.status_code == 200 and res.json().get("code") == "OK":
        print(f"[OK] 用户 {username} 已禁用")
        return res.json()
    else:
        print(f"[FAIL] 用户 {username} 禁用失败：{res.json()}")
        return None


def main():
    """禁用所有用户"""
    global public
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    print("=" * 60)
    print("开始禁用用户...")
    print(f"用户数量：{len(USERS_TO_DISABLE)}")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for i, username in enumerate(USERS_TO_DISABLE, 1):
        print(f"\n[{i}/{len(USERS_TO_DISABLE)}] 正在禁用用户：{username}")
        # 尝试 v1 API
        result = disable_user_v1(username)
        if result:
            success_count += 1
        else:
            # 如果 v1 失败，尝试 v3
            print(f"  尝试 v3 API...")
            result = disable_user_v3(username)
            if result:
                success_count += 1
            else:
                fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"禁用完成！成功：{success_count}/{len(USERS_TO_DISABLE)}，失败：{fail_count}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    finally:
        if 'public' in globals():
            public.teardown()
