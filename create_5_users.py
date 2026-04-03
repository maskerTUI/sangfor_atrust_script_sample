import sys
import os
import time
import random
import string

# 目录域配置
DIRECTORY_DOMAIN = "local"

# 中国常见姓氏及对应拼音
SURNAMES = [
    ('王', 'wang'), ('李', 'li'), ('张', 'zhang'), ('刘', 'liu'), ('陈', 'chen'),
    ('杨', 'yang'), ('黄', 'huang'), ('赵', 'zhao'), ('周', 'zhou'), ('吴', 'wu'),
    ('徐', 'xu'), ('孙', 'sun'), ('马', 'ma'), ('朱', 'zhu'), ('胡', 'hu'),
    ('郭', 'guo'), ('何', 'he'), ('高', 'gao'), ('林', 'lin'), ('罗', 'luo')
]

# 中国常见名字用字及对应拼音
FIRST_NAMES = [
    ('伟', 'wei'), ('芳', 'fang'), ('娜', 'na'), ('敏', 'min'), ('静', 'jing'),
    ('丽', 'li'), ('强', 'qiang'), ('磊', 'lei'), ('洋', 'yang'), ('艳', 'yan'),
    ('勇', 'yong'), ('军', 'jun'), ('杰', 'jie'), ('娟', 'juan'), ('涛', 'tao'),
    ('明', 'ming'), ('超', 'chao'), ('秀英', 'xiuying'), ('霞', 'xia'), ('平', 'ping'),
    ('刚', 'gang'), ('桂英', 'guiying'), ('华', 'hua'), ('鹏', 'peng'), ('辉', 'hui'),
    ('宇', 'yu'), ('浩', 'hao'), ('阳', 'yang'), ('晨', 'chen'), ('熙', 'xi'),
    ('萱', 'xuan'), ('颖', 'ying'), ('婷', 'ting'), ('博', 'bo'), ('轩', 'xuan'),
    ('子', 'zi'), ('涵', 'han'), ('欣', 'xin'), ('怡', 'yi'), ('佳', 'jia'),
    ('雨', 'yu'), ('嘉', 'jia'), ('思', 'si'), ('雅', 'ya'), ('梦', 'meng'),
    ('梓', 'zi'), ('一', 'yi'), ('可', 'ke'), ('诗', 'shi')
]


def generate_phone_number():
    """生成中国手机号"""
    prefixes = ['138', '139', '158', '159', '188', '189', '177', '199', '133', '153']
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices(string.digits, k=8))
    return prefix + suffix


def generate_realistic_user():
    """生成真实感的用户信息"""
    surname_chinese, surname_pinyin = random.choice(SURNAMES)
    name_chinese, name_pinyin = random.choice(FIRST_NAMES)
    display_name = surname_chinese + name_chinese
    phone = generate_phone_number()
    # 邮箱使用拼音
    email_base = surname_pinyin + name_pinyin + str(random.randint(10, 99))
    email_domains = ['qq.com', '163.com', 'gmail.com', 'outlook.com']
    email = email_base + '@' + random.choice(email_domains)
    return {
        'display_name': display_name,
        'phone': phone,
        'email': email
    }


def generate_strong_password(length=16):
    """生成随机强密码"""
    password_chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")
    ]
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password_chars += random.choices(all_chars, k=length-4)
    random.shuffle(password_chars)
    return ''.join(password_chars)


def create_user(name: str, password: str, group_id: str,
                status=None, inherit_group=None, description=None,
                phone=None, email=None, auth_compose_id="",
                expired_time=None, pwd_model="rsa", user_policy_id="",
                display_name=None) -> dict:
    """创建本地用户"""
    path = "/api/v1/localUser/createUser"

    body = {
        "name": name,
        "password": password,
        "groupId": group_id,
    }
    
    if user_policy_id:
        body["userPolicyId"] = user_policy_id

    if phone is not None:
        body["phone"] = phone
    if description is not None:
        body["description"] = description
    if email is not None:
        body["email"] = email
    if status is not None:
        body["status"] = status
    if inherit_group is not None:
        body["inheritGroup"] = inherit_group
    if expired_time is not None:
        body["expiredTime"] = expired_time
    if display_name is not None:
        body["displayName"] = display_name

    body["pwdModel"] = pwd_model

    if pwd_model == "rsa":
        body['password'] = public.encrypt(password)

    res = public.post(path, body)
    print(f"请求体：{body}")
    if res.status_code == 200 and res.json()["code"] == 0:
        public.pretty_print_json(res.json(), f"新建本地用户 ({name}) 成功：")
        return res.json()
    else:
        print("API 返回:", res.json())
        error_msg = res.json().get("msg", res.text)
        if "已存在" in error_msg:
            print(f"⚠️  用户 {name} 已存在，跳过")
            return None
        raise Exception('新建本地用户失败，原因：%s，错误码：%s' % (error_msg, res.json().get("code", res.status_code)))


def teardown():
    if not public.teardown():
        return


def main():
    """创建 5 个用户"""
    global public
    work_dir = os.sep.join([os.path.dirname(__file__), ".."])
    sys.path.append(work_dir)
    import public
    
    # 组织架构 ID
    group_id = "f2246260-2996-11f1-8b98-8f338082c4f7"  # /api 测试
    
    # 计算过期时间（当前时间 + 1 年）
    expired_time_ms = str(int(time.time() * 1000) + 365 * 24 * 60 * 60 * 1000)
    expire_date = time.strftime('%Y-%m-%d', time.localtime(time.time() + 365*24*60*60))
    print(f"账号有效期：{expire_date}")
    print(f"所属组织：/api 测试 (ID: {group_id})")
    print("=" * 60)
    
    # 生成 5 个用户
    users_to_create = []
    for i in range(5):
        user_info = generate_realistic_user()
        username = user_info['phone']  # 用户名用手机号
        password = generate_strong_password(16)
        users_to_create.append({
            'username': username,
            'password': password,
            'display_name': user_info['display_name'],
            'phone': user_info['phone'],
            'email': user_info['email']
        })
    
    # 打印用户信息表
    print("\n待创建用户列表：")
    print(f"{'用户名':<15} {'显示名':<10} {'手机号':<15} {'邮箱':<30} {'密码':<20}")
    print("-" * 90)
    for u in users_to_create:
        print(f"{u['username']:<15} {u['display_name']:<10} {u['phone']:<15} {u['email']:<30} {u['password']:<20}")
    print("-" * 90)
    
    print("\n开始创建用户...\n")
    
    # 创建用户
    created_users = []
    for i, user in enumerate(users_to_create, 1):
        print(f"[{i}/5] 正在创建用户：{user['username']}")
        try:
            result = create_user(
                name=user['username'],
                password=user['password'],
                group_id=group_id,
                status=1,
                phone=user['phone'],
                email=user['email'],
                display_name=user['display_name'],
                expired_time=expired_time_ms,
                pwd_model="clear"
            )
            if result:
                created_users.append(user)
                print(f"[OK] 用户 {user['username']} 创建成功\n")
            else:
                print(f"[SKIP] 用户 {user['username']} 已存在，跳过\n")
        except Exception as e:
            print(f"[FAIL] 用户 {user['username']} 创建失败：{e}\n")
    
    print("=" * 60)
    print(f"创建完成！成功：{len(created_users)}/5")
    
    # 打印成功创建的用户密码（方便记录）
    if created_users:
        print("\n成功创建的用户及密码（请妥善保存）：")
        print(f"{'用户名':<15} {'显示名':<10} {'密码':<20}")
        print("-" * 50)
        for u in created_users:
            print(f"{u['username']:<15} {u['display_name']:<10} {u['password']:<20}")


if __name__ == "__main__":
    try:
        main()
    finally:
        teardown()
