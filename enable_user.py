import sys
import os


def enable_user(user_id: str) -> dict:
    """
    启用用户
    接口：编辑用户（通过 ID）
    """
    path = "/api/v2/localUser/editUserById"
    body = {
        "id": user_id,
        "status": 1,  # 1=启用，0=禁用
        "pwdModel": "clear",  # 不需要密码，明文模式
    }
    res = public.post(path, body)
    if res.status_code == 200 and res.json()["code"] == 0:
        print("用户 (%s) 启用成功：" % user_id)
        public.pretty_print_json(res.json())
        return res.json()
    else:
        raise Exception('启用用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


def disable_user(user_id: str) -> dict:
    """
    禁用用户
    """
    path = "/api/v2/localUser/editUserById"
    body = {
        "id": user_id,
        "status": 0,  # 0=禁用
        "pwdModel": "clear",
    }
    res = public.post(path, body)
    if res.status_code == 200 and res.json()["code"] == 0:
        print("用户 (%s) 禁用成功：" % user_id)
        public.pretty_print_json(res.json())
        return res.json()
    else:
        raise Exception('禁用用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


def query_user_by_name(username: str) -> dict:
    """
    查询用户信息（通过用户名）
    """
    path = "/api/v1/localUser/queryUser"
    query = {"name": username, "groupPath": "/"}
    res = public.get(path, query)
    if res.status_code == 200 and res.json()["code"] == 0:
        print("查询用户 (%s) 成功：" % username)
        public.pretty_print_json(res.json())
        return res.json()
    else:
        raise Exception('查询用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# ---------------- demo 示例 --------------
def example_enable_gbm():
    """
    启用 gbm 用户
    """
    # gbm 用户的 ID 和用户名
    user_id = "7026fb30-da7f-11f0-a1f5-d30ce18473ba"
    username = "gbm"
    
    print("=" * 60)
    print("步骤 1: 查询当前用户状态")
    print("=" * 60)
    try:
        res = query_user_by_name(username)
        inner = res.get("data", {}).get("data", [])
        if inner:
            u = inner[0]
            print(f"当前状态：status={u.get('status')} (0=禁用，1=启用)")
    except Exception as e:
        print("查询失败:", e)
    
    print("\n" + "=" * 60)
    print("步骤 2: 启用用户")
    print("=" * 60)
    try:
        enable_user(user_id)
    except Exception as e:
        print("启用失败:", e)
    
    print("\n" + "=" * 60)
    print("步骤 3: 再次查询确认状态")
    print("=" * 60)
    try:
        res = query_user_by_name(username)
        inner = res.get("data", {}).get("data", [])
        if inner:
            u = inner[0]
            print(f"当前状态：status={u.get('status')} (0=禁用，1=启用)")
    except Exception as e:
        print("查询失败:", e)


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    example_enable_gbm()
