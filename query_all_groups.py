import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def query_all_groups(page_size: int = 20, page_index: int = 1, 
                     search_by_path: str = None, recursive: int = 1,
                     fuzzy_match: str = None) -> dict:
    """
    查询组织架构列表
    接口：/api/v3/group/queryAll
    
    参数说明：
    - directoryDomain: 用户目录唯一标识（如 "local"）- 必填
    - pageSize: 分页大小，默认 20，范围 0 < pageSize <= 5000（可选）
    - pageIndex: 分页索引，默认 1，范围 0 < pageIndex <= 1000000（可选）
    - searchByPath: 根据组织架构路径精确搜索其下的子组织架构（可选）
    - recursive: 是否递归搜索子组织，1-递归 (默认)，0-不递归（可选）
    - fuzzyMatch: 模糊搜索组织架构名称（可选）
    """
    path = "/api/v3/group/queryAll"
    
    # 构建请求体
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "pageSize": page_size,
        "pageIndex": page_index,
    }
    
    # 可选参数
    if search_by_path:
        body["searchByPath"] = search_by_path
    if recursive is not None:
        body["recursive"] = recursive
    if fuzzy_match:
        body["fuzzyMatch"] = fuzzy_match
    
    res = public.post(path, body, query={"lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('查询组织架构列表失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 默认参数
    page_size = 20
    page_index = 1
    search_by_path = None
    recursive = 1
    fuzzy_match = None
    
    # 解析命令行参数
    # 用法：python query_all_groups.py [page_size] [page_index] [search_path] [recursive]
    # 示例：
    #   python query_all_groups.py
    #   python query_all_groups.py 50 1
    #   python query_all_groups.py 20 1 "/外部组织" 1
    #   python query_all_groups.py 20 1 "" 1 "客服"
    
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
    
    if len(sys.argv) > 3 and sys.argv[3]:
        search_by_path = sys.argv[3]
    
    if len(sys.argv) > 4:
        try:
            recursive = int(sys.argv[4])
        except ValueError:
            print("错误：recursive 必须是 0 或 1")
            sys.exit(1)
    
    if len(sys.argv) > 5 and sys.argv[5]:
        fuzzy_match = sys.argv[5]
    
    print("查询组织架构列表")
    print("目录域：%s" % DIRECTORY_DOMAIN)
    print("每页数量：%d, 页码：%d" % (page_size, page_index))
    if search_by_path:
        print("搜索路径：%s" % search_by_path)
    print("递归搜索：%s" % ("是" if recursive == 1 else "否"))
    if fuzzy_match:
        print("模糊匹配：%s" % fuzzy_match)
    print("=" * 80)
    
    query_all_groups(page_size, page_index, search_by_path, recursive, fuzzy_match)
