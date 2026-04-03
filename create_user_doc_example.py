import sys
import os
import time
import json

# 目录域配置
DIRECTORY_DOMAIN = "local"


def create_user_v3(name: str, display_name: str, phone: str, email: str,
                   group_key: str, group_data: str, status: int = 1, 
                   expired_time: str = None, external_id: str = None) -> dict:
    """
    创建用户 - v3 API
    接口：/api/v3/user/create
    根据 API 文档示例格式
    """
    path = "/api/v3/user/create"
    
    body = {
        "directoryDomain": DIRECTORY_DOMAIN,
        "name": name,
        "group": {
            "key": group_key,
            "data": group_data
        },
        "externalId": external_id if external_id else f"ext_{name}",
        "inheritGroup": 1,  # 继承所属组的资源授权
        "displayName": display_name,
        "description": "通过 openAPI v3 创建",
        "status": status,
        "phone": phone,
        "email": email,
    }
    
    if expired_time is not None:
        body["expiredTime"] = expired_time
    
    # 添加 dataSource（可选）
    body["dataSource"] = {
        "description": "local",
        "email": "local",
        "phone": "local",
        "status": "server",
        "displayName": "server",
        "expiredTime": "server"
    }
    
    res = public.post(path, body=body, query={"lang": "zh-CN"})
    print(f"请求体：{json.dumps(body, indent=2, ensure_ascii=False)}")
    print(f"API 响应状态码：{res.status_code}")
    print(f"API 响应内容：{json.dumps(res.json(), indent=2, ensure_ascii=False)}")
    
    if res.status_code == 200 and res.json().get("code") == "OK":
        print("创建用户成功！")
        return res.json()
    else:
        print(f"创建用户失败")
        return None


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 用户信息
    name = "13800138000"
    display_name = "李思"
    phone = "13800138000"
    email = "123456@qq.com"
    
    # 组织架构：根组织
    group_key = "id"  # 使用 id 作为 key
    group_data = "root"  # 根组织 ID
    
    # 计算过期时间（当前时间 + 1 年，13 位毫秒时间戳）
    expired_time_ms = str(int(time.time() * 1000) + 365 * 24 * 60 * 60 * 1000)
    expire_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 365*24*60*60))
    print(f"过期时间：{expired_time_ms} (对应日期：{expire_date})")
    print(f"组织架构：{group_key} = {group_data}")
    
    print(f"\n=== 正在创建用户：{name} ===")
    
    result = create_user_v3(
        name=name,
        display_name=display_name,
        phone=phone,
        email=email,
        group_key=group_key,
        group_data=group_data,
        status=1,
        expired_time=expired_time_ms,
        external_id="ext_13800138000"
    )
    
    if not result:
        print("\n接口失败")
        sys.exit(1)
