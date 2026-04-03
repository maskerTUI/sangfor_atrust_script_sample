import sys
import os
import time
import random
import string


def query_group_by_path(group_path: str) -> dict:
    """
    基本接口：
    查询组织机构信息
    接口参数详细信息，请参考 openAPI 接口文档
    """
    path = "/api/v1/localUserGroup/queryGroupByPath"
    query = {
        "path": group_path,
    }
    res = public.get(path, query)
    if res.status_code == 200 and res.json()["code"] == 0:
        public.pretty_print_json(res.json(), "查询组织机构 (%s) 成功：" % group_path)
        return res.json()
    else:
        raise Exception('查询组织机构失败，原因：%s，错误码：%s' % (res.text, res.status_code))


def generate_strong_password(length=16):
    """
    生成随机强密码
    包含大小写字母、数字、特殊字符
    """
    # 确保包含各类字符
    password_chars = [
        random.choice(string.ascii_uppercase),  # 大写字母
        random.choice(string.ascii_lowercase),  # 小写字母
        random.choice(string.digits),           # 数字
        random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")  # 特殊字符
    ]
    # 剩余字符随机选择
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password_chars += random.choices(all_chars, k=length-4)
    # 打乱顺序
    random.shuffle(password_chars)
    return ''.join(password_chars)


def create_user(name: str, password: str, group_id: str,
                status=None, inherit_group=None, description=None,
                phone=None, email=None, auth_compose_id="",
                expired_time=None, pwd_model="rsa", user_policy_id="",
                display_name=None) -> dict:
    """
    基本接口：
    创建本地用户
    接口参数详细信息，请参考 openAPI 接口文档
    """
    path = "/api/v1/localUser/createUser"

    # 必须参数
    body = {
        "name": name,
        "password": password,
        "groupId": group_id,
    }
    
    # 添加可选的必须参数，如果为空则不传
    if user_policy_id:
        body["userPolicyId"] = user_policy_id

    # 非必须参数
    if phone is not None:
        body["phone"] = phone
    if description is not None:
        body["description"] = description
    if email is not None:
        body["email"] = email
    if status is not None:
        # 启用状态：0 禁用，1 启用，默认禁用
        body["status"] = status
    if inherit_group is not None:
        # 继承所属组的资源授权：0 不继承，1 继承，默认继承用户组的资源
        body["inheritGroup"] = inherit_group
    if expired_time is not None:
        # 过期时间，13 位长度的 Unix 时间戳，'0'表示永不过期，，默认永不过期
        body["expiredTime"] = expired_time
    if display_name is not None:
        # 显示名
        body["displayName"] = display_name

    # pwdModel: 密码传输时的加密算法，"rsa"为 RSA 非对称加密，"clear"为明文，默认为"clear"
    # 虽然是非必须参数，但是强烈建议您使用"rsa"模式传输密码
    body["pwdModel"] = pwd_model

    if pwd_model == "rsa":
        # 从控制台查询 rsa 公钥后对密码字段进行加密
        body['password'] = public.encrypt(password)

    res = public.post(path, body)
    print("请求体:", body)
    if res.status_code == 200 and res.json()["code"] == 0:
        public.pretty_print_json(res.json(), "新建本地用户 (%s) 成功：" % name)
        return res.json()
    else:
        print("API 返回:", res.json())
        raise Exception('新建本地用户失败，原因：%s，错误码：%s' % (res.json().get("msg", res.text), res.json().get("code", res.status_code)))


def teardown():
    if not public.teardown():
        return


# ---------------- demo 示例 --------------
def example1_create_local_user():
    """
    创建本地用户
    """
    # ------------- EXAMPLE 1 -------------
    # 创建一个本地用户
    # 用户名：13800138000，密码为：随机强密码
    # 手机号：13800138000，所属组织机构：/api 测试
    # 显示名：李思，邮箱：123456@qq.com
    # 过期时间：当前时间 + 1 年
    # ---------------- INPUT -----------------
    name = "13800138000"
    password = generate_strong_password(16)  # 生成 16 位随机强密码
    phone = "13800138000"
    email = "123456@qq.com"
    display_name = "李思"
    group_id = "f2246260-2996-11f1-8b98-8f338082c4f7"  # /api 测试组的 ID
    
    # 计算过期时间（当前时间 + 1 年，13 位毫秒时间戳）
    expired_time_ms = str(int(time.time() * 1000) + 365 * 24 * 60 * 60 * 1000)
    expire_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 365*24*60*60))
    print(f"过期时间：{expired_time_ms} (对应日期：{expire_date})")
    print(f"生成密码：{password}")
    
    # --------------- EXEC ----------------
    # step1: 创建用户
    # 启用状态设置为 1，启用
    try:
        create_user(name, password, group_id=group_id, 
                    status=1, 
                    phone=phone, 
                    email=email,
                    display_name=display_name,
                    expired_time=expired_time_ms,
                    pwd_model="clear")
    except Exception as e:
        error_msg = str(e)
        if "已存在" in error_msg or "already exists" in error_msg:
            print(f"用户已存在，跳过创建")
            print(f"密码已生成，请手动更新用户密码：{password}")
        else:
            raise


# 主入口
if __name__ == "__main__":
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    try:
        example1_create_local_user()
    finally:
        # 清理演示代码对控制台的配置
        teardown()
