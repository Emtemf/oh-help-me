# 安全检查规则参考

## 存量代码规则

### 核心原则

- MUST: 新建文件严格遵循规范
- MUST: 修改已有文件时，只改用户要求的部分，不扩散
- MUST NOT: 不主动改用户没要求改的东西

### 判断方式：git diff

| git diff 状态 | 含义 | 行为 |
|-------------|------|-----|
| `A` (Added) | 新建文件 | 严格检查安全漏洞 |
| `M` (Modified) | 修改已有文件 | 不检查安全问题 |
| 不在 diff 里 | 存量文件未动 | 不检查 |

### 检查项

| 问题 | 模式 | 严重级别 |
|------|------|----------|
| SQL 注入 | MyBatis `${}` | 🔴 CRITICAL |
| 硬编码密钥 | `password = "xxx"`, `apiKey = "xxx"` | 🔴 CRITICAL |
| 不安全反序列化 | `ObjectInputStream` | 🔴 CRITICAL |
