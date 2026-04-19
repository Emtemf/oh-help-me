---
name: architecture-check
description: Java Clean Architecture 检查。检查依赖方向、对象边界、命名规范。当检查架构、检查边界、architecture check 时使用。
context: fork
agent: Explore
---

# 架构检查任务

## 检查范围
$ARGUMENTS

## Quick Reference

| 规则 | 加载时机 | 文件 |
|------|----------|------|
| 边界隔离规则 | 检查依赖方向、对象边界时 | `reference/boundary.md` |
| 存量代码规则 | 判断 git diff 状态时 | `reference/legacy-code.md` |

## Step 1: 确定检查文件

如果 `$ARGUMENTS` 为空：
```bash
git diff --name-status HEAD
```

根据 `reference/legacy-code.md`：
- 状态 `A`（新增）→ 严格检查
- 状态 `M`（修改）→ 跳过架构检查
- 不在 diff 中 → 跳过所有检查

如果 `$ARGUMENTS` 指定了路径，只检查该路径下的新增文件。

## Step 2: 执行检查

对每个新增的 `.java` 文件，根据 `reference/boundary.md` 执行：

### 依赖方向检查
- 领域层 import 基础设施层 → 🔴 CRITICAL
- 应用层 import 接口层 Req/Rsp → 🔴 CRITICAL

### 对象边界检查
- Req/Rsp 传递到应用层/领域层 → 🔴 CRITICAL
- Entity 泄露到基础设施层外 → 🔴 CRITICAL

## Step 3: 输出结果（结论先行）

只输出发现的问题，格式：
```
## 架构检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
```

无新增文件或无问题则输出：✅ 未发现架构违规问题
