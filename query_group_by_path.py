import sys
import os
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def query_group_by_path(full_path: str) -> dict:
    """
    查询组织架构详情（基于路径）
    接口：/api/v3/group/queryByFullPath
    
    参数说明：
    - directoryDomain: 用户目录唯一标识（如 "local"）- 必填
    - fullPath: 全路径（如 "/" 表示根目录）- 必填
    """
    path = "/api/v3/group/queryByFullPath"
    res = public.get(path, query={"directoryDomain": DIRECTORY_DOMAIN, "fullPath": full_path, "lang": "zh-CN"})
    if res.status_code == 200 and res.json()["code"] == "OK":
        print(json.dumps(res.json(), indent=2, ensure_ascii=False))
        return res.json()
    else:
        raise Exception('查询组织架构失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 从命令行参数获取路径
    if len(sys.argv) < 2:
        print("用法：python query_group_by_path.py <组织架构路径>")
        print("示例：")
        print("  python query_group_by_path.py /")
        print("  python query_group_by_path.py /外部组织")
        print("  python query_group_by_path.py /api 测试")
        sys.exit(1)
    
    full_path = sys.argv[1]
    query_group_by_path(full_path)
