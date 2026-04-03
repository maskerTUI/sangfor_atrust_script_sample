import os
import time
import json
import hashlib
import hmac
import requests
import uuid
import urllib3
import config
import rsa

def cal_signature(key: str, url: str, query=None, body=None) -> str:
    """
    计算请求体的签名:
    签名字符串分为两个部分：1. 路径部分 path；2. 参数部分 query, body
    path 路径，例如： /api/v1/admin/login
    query 参数，对 key 按 ascii 排序后拼接的字符串，例如：password=123&username=sf
    body 参数，通常认为是一个 json 字符串，为了跨语言兼容，这里必须是严格的 json 格式，逗号和分号后不能有空格和换行，如：{"key1":"value1"}
    路径与参数之间用'?'拼接，参数与参数之间拼接用'&'，例如：
    签名字符串为：sign_str = ${path}?${query}&${body}，其中${xx}表示变量
    """

    # 从 url 中解析 path 路径
    path = urllib3.util.url.parse_url(url).path

    # 按规则拼接 query 参数的 kv_str("k=v")
    params_list = []
    if query is not None:
        sorted_query = sorted(query.items(), key=lambda x: x[0])
        for k, v in sorted_query:
            params_list.append(k + "=" + v)

    # 准备 body 参数，严格 json 字符串
    if body is not None:
        params_list.append(json.dumps(body, ensure_ascii=False, separators=(',', ':')))

    if len(params_list):
        str_to_sign = path + "?" + "&".join(params_list)
    else:
        # 如果不存在参数，以路径作为被签名的内容
        str_to_sign = path

    # 签名
    sig = hmac.new(key=key.encode('UTF-8'), digestmod=hashlib.sha256)
    sig.update(str_to_sign.encode('UTF-8'))
    return sig.hexdigest()


def prepare_auth_headers(url: str, query=None, body=None) -> dict:
    """
    准备 Open API 的请求鉴权头部：
    x-ca-key: API ID，从控制台获取
    x-ca-sign: 请求签名，用 API 密钥等拼接出的字符串对请求体内容计算出的签名
    x-ca-timestamp: 时间戳，长度为 10 的整数字符串
    x-ca-nonce: 随机数，数字字母加横线的字符串，长度 2~128 位
    """
    app_id = config.API_ID
    app_secret = config.API_SECRET
    # 获取十位时间戳
    timestamp = str(int(round(time.time())))
    # 数字字母加横线的字符串，长度 2~128 位，这里我们使用 uuid/v4 生成这样一个字符串
    nonce = str(uuid.uuid4())

    # 按照下面规则拼接签名密钥
    key = "appId=%s&appSecret=%s&timestamp=%s&nonce=%s" % (app_id, app_secret, timestamp, nonce)
    sign = cal_signature(key, url, query, body)

    return {
        "x-ca-key": app_id,
        "x-ca-timestamp": timestamp,
        "x-ca-nonce": nonce,
        "x-ca-sign": sign,
    }


def get(path: str, query=None, headers=None) -> requests.Response:
    """
    get 请求接口，该接口封装了 openAPI 鉴权的请求头部
    """

    if headers is None:
        headers = dict()
    url = config.CONSOLE_ADDRESS + path
    auth_headers = prepare_auth_headers(url, query)
    headers.update(auth_headers)

    return requests.get(url=url, headers=headers, params=query, verify=False)


def post(path: str, body=None, headers=None, query=None) -> requests.Response:
    """
    post 请求接口，该接口封装了 openAPI 鉴权的请求头部
    """

    if headers is None:
        headers = dict()
    url = config.CONSOLE_ADDRESS + path
    auth_headers = prepare_auth_headers(url, body=body, query=query)
    headers.update(auth_headers)
    
    # 使用 data 参数而不是 json 参数，确保 body 格式与签名一致
    if body is not None:
        body_str = json.dumps(body, ensure_ascii=False, separators=(',', ':'))
        headers['Content-Type'] = 'application/json; charset=utf-8'
        return requests.post(url=url, headers=headers, data=body_str, params=query, verify=False)
    else:
        return requests.post(url=url, headers=headers, params=query, verify=False)


def get_console_config():
    """
    获取控制台基本配置接口，包含：rsa 加密信息
    """

    path = '/api/v1/admin/getConfig'
    res = get(path)
    return res.json()


def encrypt(password: str) -> str:
    """
    获取控制台 rsa 公钥，对用户密码进行加密
    """
    # 获取加密公钥信息
    res = get_console_config()

    # 防重放随机数
    anti_replay_rand = res['data']['crypto']['antiReplayRand']

    # 公钥
    pubKey = res['data']['crypto']['pubKey']
    pubKeyExp = res['data']['crypto']['pubKeyExp']
    pubKey = int(pubKey, 16)
    pubKeyExp = int(pubKeyExp)
    antiReplayRand = res['data']['crypto']['antiReplayRand']
    
    message = password + '_' + anti_replay_rand
    rsa_pubkey = rsa.PublicKey(pubKey, pubKeyExp)
    crypto = rsa.encrypt(message.encode(), rsa_pubkey)
    return crypto.hex()


def pretty_print_json(data=None, msg=None, quiet=None):
    """
    漂亮打印 json 数据
    """
    if quiet is None:
        quiet = not config.DEBUG_PRINT_RESP
    if quiet:
        return
    if data is None:
        return
    if msg is None:
        print(json.dumps(data))
    else:
        print("%s\n%s" % (msg, json.dumps(data, indent=2, ensure_ascii=False)))


def teardown() -> bool:
    """
    是否需要执行 teardown
    """
    return config.ENABLE_TEARDOWN
