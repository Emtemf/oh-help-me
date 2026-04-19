# 质量检查规则参考

## 存量代码规则

### 核心原则

- MUST: 新建文件严格遵循规范
- MUST: 修改已有文件时，只改用户要求的部分，不扩散
- MUST NOT: 不主动改用户没要求改的东西

### 判断方式：git diff

| git diff 状态 | 含义 | 行为 |
|-------------|------|-----|
| `A` (Added) | 新建文件 | 严格检查质量问题 |
| `M` (Modified) | 修改已有文件 | 不检查质量问题 |
| 不在 diff 里 | 存量文件未动 | 不检查 |

### 检查项

| 问题 | 阈值 | 严重级别 |
|------|------|----------|
| 方法长度超过限制 | > 50 行 | 🟡 WARNING |
| 空 catch 块 | `catch (Exception e) {}` | 🔴 CRITICAL |
| printStackTrace | `e.printStackTrace()` | 🟡 WARNING |
