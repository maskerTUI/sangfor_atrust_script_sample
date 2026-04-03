import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def query_user_by_name(username: str) -> dict:
    """
    查询用户信息（基于用户名）
    接口：/api/v3/user/queryByName
    
    参数说明：
    - directoryDomain: 用户目录唯一标识（如 "local"）
    - name: 用户名
    """
    path = "/api/v3/user/queryByName"
    res = public.get(path, query={"directoryDomain": DIRECTORY_DOMAIN, "name": username, "lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('查询用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 从命令行参数获取用户名
    if len(sys.argv) < 2:
        print("用法：python query_user_v3.py <用户名>")
        print("示例：python query_user_v3.py gbm")
        sys.exit(1)
    
    username = sys.argv[1]
    query_user_by_name(username)
