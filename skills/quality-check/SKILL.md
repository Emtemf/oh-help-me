---
name: quality-check
description: Java 代码质量检查。检查命名、方法长度、异常处理。当检查质量、quality check 时使用。
context: fork
agent: Explore
model: haiku
---

# 质量检查任务

## 检查范围
$ARGUMENTS

## Quick Reference

| 规则 | 加载时机 | 文件 |
|------|----------|------|
| 存量代码规则 | 判断 git diff 状态时 | `reference/legacy-code.md` |

## Step 1: 确定检查文件

如果 `$ARGUMENTS` 为空：
```bash
git diff --name-status HEAD
```

根据 `reference/legacy-code.md`：
- 状态 `A`（新增）→ 严格检查
- 状态 `M`（修改）→ 不检查质量问题
- 不在 diff 中 → 跳过所有检查

如果 `$ARGUMENTS` 指定了路径，只检查该路径下的新增文件。

## Step 2: 执行检查

对所有新增的 `.java` 文件执行：

- 方法长度 > 50 行 → 🟡 WARNING
- 空 catch 块 → 🔴 CRITICAL
- printStackTrace → 🟡 WARNING

## Step 3: 输出结果（结论先行）

只输出发现的问题，格式：
```
## 质量检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
```

无新增文件或无问题则输出：✅ 未发现质量问题