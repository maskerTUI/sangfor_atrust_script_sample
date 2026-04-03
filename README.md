# 深信服零信任 (aTrust) OpenAPI Python 脚本集合

这是一组用于管理深信服零信任 (aTrust) 设备的 Python 脚本，基于官方 OpenAPI 开发。

## ⚠️ 重要提示

**本仓库不包含任何敏感信息！** 在使用前，请先配置您的 `config.py` 文件。

## 功能列表

### 用户管理
- `query_user_v3.py` - 查询单个用户信息
- `enable_user_v3.py` - 启用/禁用用户
- `query_all_users_v3.py` - 查询所有用户列表
- `query_online_users.py` - 查询在线用户
- `query_group_by_path.py` - 查询组织架构详情

### 组织管理
- `query_org_by_id.py` - 根据 ID 查询组织
- `query_root_org.py` - 查询根组织
- `query_group_test.py` - 组织查询测试

### 用户创建
- `create_user_v3.py` - 创建新用户 (v3 API)
- `create_user.py` - 创建用户
- `create_user_final.py` - 最终版用户创建脚本
- `create_user_root.py` - 创建根用户
- `create_user_v1.py` - 创建用户 (v1 API)
- `create_user_v3_try.py` - v3 用户创建测试

### 批量操作
- `bulk_delete_user_by_name.py` - 批量删除用户

### 工具脚本
- `extract_api.py` - API 提取工具
- `public.py` - API 请求封装（包含签名逻辑）

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API 密钥

编辑 `config.py` 文件，填写您的深信服零信任控制台信息：

```python
# 控制台地址
CONSOLE_ADDRESS = 'https://your-atrust-server:4433'

# Open API ID（从控制台获取）
API_ID = 'your-api-id'

# Open API 密钥（从控制台获取）
API_SECRET = 'your-api-secret'
```

### 3. 获取 API 凭证

1. 登录深信服零信任控制台 (aTrust)
2. 进入「系统管理」>「OpenAPI 管理」
3. 创建新的 API 应用，获取 API ID 和 API 密钥

## 使用示例

### 查询用户

```bash
python query_user_v3.py 张三
```

### 启用/禁用用户

```bash
# 启用用户
python enable_user_v3.py enable 张三

# 禁用用户
python enable_user_v3.py disable 张三
```

### 查询在线用户

```bash
# 查询所有在线用户（默认 20 条）
python query_online_users.py

# 查询 50 条记录
python query_online_users.py 50

# 搜索特定用户
python query_online_users.py 20 1 张三
```

### 查询组织架构

```bash
# 查询根目录
python query_group_by_path.py /

# 查询特定组织路径
python query_group_by_path.py /外部组织
```

## API 签名机制

本脚本使用深信服零信任的 OpenAPI 签名机制：

1. **请求头**：
   - `x-ca-key`: API ID
   - `x-ca-sign`: 请求签名
   - `x-ca-timestamp`: 时间戳
   - `x-ca-nonce`: 随机数

2. **签名算法**：
   - 使用 HMAC-SHA256
   - 签名字符串格式：`path?query&body`
   - 密钥格式：`appId=xxx&appSecret=xxx&timestamp=xxx&nonce=xxx`

详细信息请参考 `public.py` 文件。

## 安全建议

1. **不要将 `config.py` 提交到版本控制系统**
   - 建议将 `config.py` 添加到 `.gitignore`
   - 使用环境变量或密钥管理服务存储敏感信息

2. **使用最小权限原则**
   - 为不同用途创建不同的 API 密钥
   - 定期轮换 API 密钥

3. **保护服务器安全**
   - 确保控制台地址使用 HTTPS
   - 限制 API 访问的 IP 白名单

## 依赖项

- `requests` - HTTP 请求库
- `rsa` - RSA 加密库（用于密码加密）
- `urllib3` - URL 处理库

## 注意事项

1. 本脚本仅支持深信服零信任 (aTrust) 设备，不适用于 SSL VPN 设备
2. API 版本可能因设备固件版本而异
3. 使用前请确保已阅读官方 OpenAPI 文档

## 参考资料

- [深信服零信任 OpenAPI 文档](https://your-atrust-server:4433)
- [官方 API 示例](https://github.com/sangfor-openapi)

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

---

**注意**: 本脚本由社区维护，与深信服官方无关。使用风险自负。
