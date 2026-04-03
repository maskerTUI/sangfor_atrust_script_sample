import sys
import os
import json


def query_user_by_name(username: str, group_path: str = "/") -> dict:
    """
    基本接口：
    查询用户信息（按用户名和组织机构路径）
    接口参数详细信息，请参考 openAPI 接口文档
    """
    path = "/api/v1/localUser/queryUser"
    query = {
        "name": username,
        "groupPath": group_path,
    }
    res = public.get(path, query)
    if res.status_code == 200 and res.json()["code"] == 0:
        public.pretty_print_json(res.json(), "查询用户 (%s) 成功：" % username)
        return res.json()
    else:
        print("API 返回:", res.json())
        raise Exception('查询用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


def query_user_list(group_id: str = "root", page: int = 1, page_size: int = 100) -> dict:
    """
    基本接口：
    查询用户列表
    接口参数详细信息，请参考 openAPI 接口文档
    """
    path = "/api/v1/localUser/queryUserList"
    query = {
        "groupId": group_id,
        "page": str(page),
        "pageSize": str(page_size),
    }
    res = public.get(path, query)
    if res.status_code == 200 and res.json()["code"] == 0:
        public.pretty_print_json(res.json(), "查询用户列表成功：")
        return res.json()
    else:
        raise Exception('查询用户列表失败，原因：%s，错误码：%s' % (res.text, res.status_code))


# ---------------- demo 示例 --------------
def example1_query_user_by_name():
    """
    按用户名查询用户
    """
    # ---------------- INPUT -----------------
    username = "zoumingluan"
    group_path = "/"  # 本地用户组根目录
    # --------------- EXEC ----------------
    try:
        res = public.get("/api/v1/localUser/queryUser", query={"name": username, "groupPath": group_path})
        data = res.json()
        print("API 返回:", json.dumps(data, indent=2, ensure_ascii=False))
        # 检查返回的数据结构
        inner_data = data.get("data", {}).get("data", [])
        if isinstance(inner_data, list) and len(inner_data) > 0:
            print("\n找到用户:")
            for u in inner_data:
                print(f"  - 姓名：{u.get('name')}, ID: {u.get('id')}, 手机号：{u.get('phone')}")
        else:
            print(f"\n未找到用户 {username}")
    except Exception as e:
        print(f"查询失败：{e}")


def example2_query_user_list():
    """
    查询用户列表
    """
    # ---------------- INPUT -----------------
    group_id = "root"  # 根目录组 ID
    page = 1
    page_size = 100
    # --------------- EXEC ----------------
    try:
        res = public.get("/api/v1/localUser/queryUserList", query={"groupId": group_id, "page": str(page), "pageSize": str(page_size)})
        data = res.json()
        print("API 返回:", json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print("查询失败:", str(e))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    print("=" * 60)
    print("示例 1: 按用户名查询用户")
    print("=" * 60)
    try:
        example1_query_user_by_name()
    except Exception as e:
        print("示例 1 失败:", str(e))
    
    print("\n" + "=" * 60)
    print("示例 2: 查询用户列表")
    print("=" * 60)
    try:
        example2_query_user_list()
    except Exception as e:
        print("示例 2 失败:", str(e))
