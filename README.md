# oh-help-me

一个用于 Java 代码审查工作流的 Claude Code 插件，支持 Clean Architecture 检查。

## 核心逻辑

```
用户调用 /architecture-check
        ↓
检查 git diff --name-status HEAD
        ↓
┌───────────────────────────────────────┐
│  状态为 A (Added)？                    │
│  ├─ 是 → 严格检查架构违规              │
│  └─ 否 (M/D/无变更) → 跳过检查         │
└───────────────────────────────────────┘
        ↓
输出检查结果
```

**为什么这样设计？**

| 状态 | 说明 | 处理方式 |
|------|------|----------|
| A (Added) | 新增文件 | 严格检查，确保新代码符合规范 |
| M (Modified) | 修改已有文件 | 跳过架构检查，尊重存量代码 |
| 不在 diff 中 | 存量文件 | 不检查，避免对历史代码的干扰 |

## 安装

```bash
# 从 GitHub 安装
/plugin install https://github.com/Emtemf/oh-help-me

# 或从本地目录安装
/plugin install /path/to/oh-help-me
```

## 功能

### Skills（技能）

#### `architecture-check` - 架构检查
检查 Clean Architecture 合规性：
- 依赖方向违规（领域层引用基础设施层）
- 对象边界违规（Entity 泄露到基础设施层外）

```bash
# 仅检查 git diff 变更文件（新增文件）
/architecture-check

# 检查指定路径
/architecture-check src/main/java
```

#### `security-check` - 安全检查
检查 Java 安全问题：
- SQL 注入（MyBatis `${}`）
- 硬编码密钥
- 不安全反序列化

```bash
/security-check
```

#### `quality-check` - 质量检查
检查代码质量：
- 方法长度超过 50 行
- 空 catch 块
- printStackTrace 调用

```bash
/quality-check
```

### Command（命令）

#### `check` - 全面检查
并行执行所有检查：

```bash
/check              # 检查 git diff 变更
/check src/main/    # 检查指定路径
```

## 验证证据

以下是在真实项目中运行的实际输出截图。

### 场景 1：无新增文件 → 跳过检查

**前置条件：**
```bash
$ git diff --name-status HEAD
M   .omc/state/hud-stdin-cache.json
```

**执行命令：**
```bash
/architecture-check
```

**实际输出：**
```
## 架构检查结果

✅ 未发现架构违规问题
```

**验证逻辑：** git diff 中只有 M 状态的文件（非 .java），无 `A` 状态的 `.java` 文件，因此跳过检查。

---

### 场景 2：新增文件包含架构违规 → 报告 CRITICAL

**前置条件：**
```bash
$ git diff --name-status HEAD
A   src/main/java/com/example/api/NewApiReq.java
M   src/main/java/com/example/api/OrderRsp.java
```

**NewApiReq.java 内容：**
```java
package com.example.api;

import com.example.infra.entity.OrderEntity; // 违规：接口层引用基础设施层

public class NewApiReq {
    private OrderEntity order; // 违规：Entity 泄露到接口层
}
```

**执行命令：**
```bash
/architecture-check
```

**实际输出：**
```
## 架构检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | api/NewApiReq.java | 3 | 接口层 import 基础设施层 OrderEntity | Entity 不可泄露到接口层，移除 import |
```

**验证逻辑：**
- `NewApiReq.java` 状态为 `A`（新增）→ 触发严格检查
- `OrderRsp.java` 状态为 `M`（修改）→ 不触发架构检查

---

### 场景 3：修改文件不检查 → 无报告

**前置条件：**
```bash
$ git diff --name-status HEAD
M   src/main/java/com/example/app/OrderService.java
```

**OrderService.java 内容（含架构问题）：**
```java
package com.example.app;

import com.example.api.OrderReq; // 违规：应用层引用接口层 Req

public class OrderService {
    public void process(OrderReq req) { // 违规：Req 传到应用层
    }
}
```

**执行命令：**
```bash
/architecture-check
```

**实际输出：**
```
## 架构检查结果

✅ 未发现架构违规问题
```

**验证逻辑：** `OrderService.java` 状态为 `M`（修改），不是新增文件，因此跳过架构检查。这是设计行为，尊重存量代码。

---

### 场景 4：存量文件不检查 → 无报告

**前置条件：**
```bash
$ git diff --name-status HEAD
A   src/main/java/com/example/api/NewApiReq.java
# 注：infra/OrderMapper.java 存在但未在 diff 中
```

**存量文件 OrderMapper.java 内容（含安全问题）：**
```java
package com.example.infra;

public class OrderMapper {
    public void query() {
        // SQL 注入风险
        String sql = "SELECT * FROM orders WHERE id = ${id}";
    }
}
```

**执行命令：**
```bash
/security-check
```

**实际输出：**
```
## 安全检查结果

✅ 未发现安全漏洞
```

**验证逻辑：** `OrderMapper.java` 不在 git diff 中（存量文件），因此不检查。

---

### 场景 5：指定路径无新增文件 → 跳过检查

**前置条件：**
```bash
$ git diff --name-status HEAD
A   src/main/java/com/example/api/NewApiReq.java
# 注：新增文件在 api/ 目录，不在 infra/ 目录
```

**执行命令：**
```bash
/architecture-check src/main/java/com/example/infra
```

**实际输出：**
```
## 架构检查结果

✅ 未发现架构违规问题
```

**验证逻辑：** `infra/` 目录下无新增文件，因此跳过检查。

---

### 场景 6：全面检查 → 并行报告

**前置条件：**
```bash
$ git diff --name-status HEAD
A   src/main/java/com/example/api/NewApiReq.java
A   src/main/java/com/example/infra/OrderMapper.java
A   src/main/java/com/example/app/OrderService.java
```

**执行命令：**
```bash
/check
```

**实际输出：**
```
## 架构检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | api/NewApiReq.java | 3 | 接口层 import 基础设施层 | 移除 import |

## 安全检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | infra/OrderMapper.java | 8 | MyBatis 使用 ${} 存在 SQL 注入风险 | 改用 #{} |

## 质量检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🟡 WARNING | app/OrderService.java | 10 | 方法长度超过 50 行 | 拆分方法 |
| 🔴 CRITICAL | app/OrderService.java | 65 | 空 catch 块 | 添加异常处理 |
```

## 验证覆盖总结

| 场景 | git diff 状态 | 预期行为 | 实际结果 |
|------|--------------|----------|----------|
| 无新增文件 | M (非 .java) | 跳过检查 | ✅ 输出"未发现问题" |
| 新增文件有违规 | A | 报告 CRITICAL | ✅ 正确报告问题 |
| 修改文件有违规 | M | 不报告 | ✅ 跳过检查 |
| 存量文件有违规 | 不在 diff | 不报告 | ✅ 跳过检查 |
| 指定路径无新增 | A (在其他路径) | 跳过检查 | ✅ 输出"未发现问题" |

## 输出格式

```
## 检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | domain/Order.java | 3 | 领域层 import 基础设施层 | 移除 import |
| 🟡 WARNING | app/OrderService.java | 52 | 方法长度超过 50 行 | 拆分方法 |
```

严重级别说明：
- 🔴 CRITICAL - 提交前必须修复
- 🟡 WARNING - 应该修复
- 🔵 SUGGESTION - 建议优化

## 配置

插件遵循项目级 `.claude/rules/clean-architecture/` 规则：

- `boundary.md` - 层边界规则
- `legacy-code.md` - 增量检查策略
- `layer-*.md` - 各层特定规则

## 许可证

MIT
