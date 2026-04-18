---
name: check
description: 对代码进行全面检查：架构边界 + 安全漏洞 + 代码质量
context: fork
agent: Explore
---

# 全面代码检查

对 $ARGUMENTS 进行全面代码检查。

## Step 1: 确定检查范围

- 如果 `$ARGUMENTS` 指定了目标，传递给各 Skill
- 如果没有指定，各 Skill 自动使用 git diff 新增文件（A 状态）

## Step 2: 并行激活三个 Skill

使用 Agent 工具并行调用：

1. **architecture-check**
2. **security-check**
3. **quality-check**

每个 Skill 使用 `context: fork` 创建隔离会话，独立执行检查。

## Step 3: 汇总检查结论

收集三个 Skill 的输出，按严重级别排序：
🔴 CRITICAL → 🟡 WARNING → 🔵 SUGGESTION

## 存量代码规则

根据 `.claude/rules/clean-architecture/legacy-code.md`：
- 只检查 git diff 中状态为 `A`（新增）的文件
- 修改已有文件（M）和存量文件不触发检查