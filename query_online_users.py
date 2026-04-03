import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def query_online_users(page_size: int = 20, page_index: int = 1, 
                       search_value: str = None, filter_type: str = None,
                       sort_by: str = None, asc: int = None) -> dict:
    """
    查询在线用户
    接口：/api/v1/monitor/getUserStatus
    
    参数说明：
    - pageSize: 每页大小，默认 20（必填）
    - pageIndex: 当前页，默认 1（必填）
    - filter: 过滤条件，可选值：all、name、displayName、userDirectoryName、groupPath、remoteIp、vip、os、browser（可选）
    - searchValue: 搜索值（可选）
    - sortBy: 排序字段，可选值：name、groupPath、browser、os、lastLoginTime、authTypeList、remoteIp、userDirectoryName、vip（可选）
    - asc: 是否升序：1 为升序、0 为降序（默认降序）（可选）
    """
    path = "/api/v1/monitor/getUserStatus"
    
    # 必填参数
    query = {
        "pageSize": str(page_size),
        "pageIndex": str(page_index),
    }
    
    # 可选参数
    if filter_type:
        query["filter"] = filter_type
    if search_value:
        query["searchValue"] = search_value
    if sort_by:
        query["sortBy"] = sort_by
    if asc is not None:
        query["asc"] = str(asc)
    
    res = public.get(path, query)
    if res.status_code == 200 and res.json()["code"] == 0:
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('查询在线用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 默认参数
    page_size = 20
    page_index = 1
    search_value = None
    filter_type = None
    sort_by = None
    asc = None
    
    # 解析命令行参数
    # 用法：python query_online_users.py [page_size] [page_index] [search_value]
    # 示例：
    #   python query_online_users.py
    #   python query_online_users.py 50 1
    #   python query_online_users.py 20 1 张三
    #   python query_online_users.py 20 1 name name
    
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
        search_value = sys.argv[3]
    
    if len(sys.argv) > 4:
        sort_by = sys.argv[4]
    
    if len(sys.argv) > 5:
        try:
            asc = int(sys.argv[5])
        except ValueError:
            print("错误：asc 必须是 0 或 1")
            sys.exit(1)
    
    print("查询在线用户")
    print("每页数量：%d, 页码：%d" % (page_size, page_index))
    if search_value:
        print("搜索值：%s" % search_value)
    if sort_by:
        print("排序字段：%s" % sort_by)
        print("排序方式：%s" % ("升序" if asc == 1 else "降序"))
    print("=" * 80)
    
    query_online_users(page_size, page_index, search_value, filter_type, sort_by, asc)
