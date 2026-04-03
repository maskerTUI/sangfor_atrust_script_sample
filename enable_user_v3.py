import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def enable_user_by_name(username: str) -> dict:
    """
    启用用户（基于用户名）
    接口：/api/v3/user/updateByName
    
    参数说明：
    - directoryDomain: 用户目录唯一标识（如 "local"）
    - name: 用户名
    - status: 1=启用，0=禁用
    """
    path = "/api/v3/user/updateByName"
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "name": username,
        "status": 1,  # 1=启用，0=禁用
    }
    res = public.post(path, body, query={"lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('启用用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


def disable_user_by_name(username: str) -> dict:
    """
    禁用用户（基于用户名）
    """
    path = "/api/v3/user/updateByName"
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "name": username,
        "status": 0,  # 0=禁用
    }
    res = public.post(path, body, query={"lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('禁用用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 从命令行参数获取用户名和操作
    if len(sys.argv) < 2:
        print("用法：python enable_user_v3.py <启用/禁用> <用户名>")
        print("示例：")
        print("  python enable_user_v3.py enable gbm")
        print("  python enable_user_v3.py disable gbm")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    username = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not username:
        print("错误：请提供用户名")
        sys.exit(1)
    
    if action == "enable":
        enable_user_by_name(username)
    elif action == "disable":
        disable_user_by_name(username)
    else:
        print("错误：操作必须是 'enable' 或 'disable'")
        sys.exit(1)
