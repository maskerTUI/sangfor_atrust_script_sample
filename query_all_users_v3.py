import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def query_all_users(page_size: int = 100, page_index: int = 1, search_by_path: str = None, recursive: int = 1) -> dict:
    """
    查询用户列表
    接口：/api/v3/user/queryAll
    
    参数说明：
    - directoryDomain: 用户目录唯一标识（如 "local"）- 必填
    - pageSize: 每页数量，默认 100
    - pageIndex: 页码，默认 1
    - searchByPath: 搜索路径（可选）
    - recursive: 是否递归，默认 1
    """
    path = "/api/v3/user/queryAll"
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "pageSize": page_size,
        "pageIndex": page_index,
        "recursive": recursive,
    }
    
    # 可选参数
    if search_by_path:
        body["searchByPath"] = search_by_path
    
    res = public.post(path, body, query={"lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('查询用户列表失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 默认参数
    page_size = 100
    page_index = 1
    search_by_path = None
    
    # 解析命令行参数
    # 用法：python query_all_users_v3.py [page_size] [page_index] [search_path]
    # 示例：
    #   python query_all_users_v3.py
    #   python query_all_users_v3.py 50 1
    #   python query_all_users_v3.py 100 1 "/外部组织"
    
    if len(sys.argv) > 1:
        try:
            page_size = int(sys.argv[1])
        except ValueError:
            print("错误：page_size 必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 2:
        try:
            page_index = int(sys.argv[2])
        except ValueError:
            print("错误：page_index 必须是数字")
            sys.exit(1)
    
    if len(sys.argv) > 3:
        search_by_path = sys.argv[3]
    
    print("查询目录域：%s" % DIRECTORY_DOMAIN)
    print("每页数量：%d, 页码：%d" % (page_size, page_index))
    if search_by_path:
        print("搜索路径：%s" % search_by_path)
    print("=" * 60)
    
    query_all_users(page_size, page_index, search_by_path)
