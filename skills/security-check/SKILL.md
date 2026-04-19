---
name: security-check
description: Java 安全检查。检查 SQL 注入、硬编码密钥、反序列化漏洞。当检查安全、security check、检查漏洞时使用。
context: fork
agent: Explore
---

# 安全检查任务

## 检查范围
$ARGUMENTS

## 规则来源

优先使用项目级规则 `.claude/rules/clean-architecture/legacy-code.md`，不存在时使用本目录下的 `legacy-code.md`。

## Step 1: 确定检查文件

如果 `$ARGUMENTS` 为空：
```bash
git diff --name-status HEAD
```

根据 `legacy-code.md` 规则：
- 状态 `A`（新增）→ 严格检查
- 状态 `M`（修改）→ 不检查安全问题
- 不在 diff 中 → 跳过所有检查

如果 `$ARGUMENTS` 指定了路径，只检查该路径下的新增文件。

## Step 2: 执行检查

对所有新增的 `.java` 文件执行：

- SQL 注入：MyBatis `${}` → 🔴 CRITICAL
- 硬编码密钥：`password = "xxx"` → 🔴 CRITICAL
- 不安全反序列化：ObjectInputStream → 🔴 CRITICAL

## Step 3: 输出结果（结论先行）

所有安全问题都是 🔴 CRITICAL

只输出发现的问题，格式：
```
## 安全检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
```

无新增文件或无问题则输出：✅ 未发现安全漏洞