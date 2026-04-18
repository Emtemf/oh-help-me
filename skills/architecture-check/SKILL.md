---
name: architecture-check
description: Java Clean Architecture 检查。检查依赖方向、对象边界、命名规范。当检查架构、检查边界、architecture check 时使用。
context: fork
agent: Explore
---

# 架构检查任务

## 检查范围
$ARGUMENTS

## Step 1: 确定检查文件

如果 `$ARGUMENTS` 为空：
```bash
git diff --name-status HEAD
```
只检查状态为 `A`（新增）的文件，跳过 `M`（修改）和存量文件。

如果 `$ARGUMENTS` 指定了路径，只检查该路径下的新增文件（git diff A 状态）。

## Step 2: 执行检查

对每个新增的 `.java` 文件执行以下检查：

### 依赖方向
- 领域层 import 基础设施层 → 🔴 CRITICAL
- 应用层 import 接口层 Req/Rsp → 🔴 CRITICAL

### 对象边界
- Req/Rsp 传递到应用层/领域层 → 🔴 CRITICAL
- Entity 泄露到基础设施层外 → 🔴 CRITICAL

## Step 3: 输出结果（结论先行）

只输出发现的问题，格式：
```
## 架构检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
```

无新增文件或无问题则输出：✅ 未发现架构违规问题

## 存量代码规则

根据 `.claude/rules/clean-architecture/legacy-code.md`：
- 新建文件（A）→ 严格检查
- 修改已有文件（M）→ 不检查架构违规
- 存量文件未动 → 不加载规则，不影响上下文