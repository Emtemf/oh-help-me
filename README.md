# oh-help-me

一个用于 Java 代码审查工作流的 Claude Code 插件，支持 Clean Architecture 检查。

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

## 设计原则

### 增量检查

遵循 `.claude/rules/clean-architecture/legacy-code.md` 规则：

| git diff 状态 | 行为 |
|--------------|------|
| `A`（新增） | 严格检查 |
| `M`（修改） | 跳过架构检查 |
| 不在 diff 中 | 跳过所有检查 |

**只检查新代码，尊重存量代码。**

### 子代理隔离

每个 skill 在隔离的子代理会话中运行：
- `context: fork` - 隔离执行上下文
- `agent: Explore` - 使用 Explore 代理扫描代码

## 输出格式

```
## 检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | domain/Order.java | 3 | 领域层 import 基础设施层 | 移除 import |
| 🟡 WARNING | app/OrderService.java | 52 | 方法长度超过 50 行 | 拆分方法 |
```

- 🔴 CRITICAL - 提交前必须修复
- 🟡 WARNING - 应该修复
- 🔵 SUGGESTION - 建议优化

## 配置

插件遵循项目级 `.claude/rules/clean-architecture/` 规则：

- `boundary.md` - 层边界规则
- `legacy-code.md` - 增量检查策略
- `layer-*.md` - 各层特定规则

## 验证示例

### 场景 1：无新增文件

```bash
$ git diff --name-status HEAD
M   .omc/state/hud-stdin-cache.json

$ /architecture-check
## 架构检查结果
✅ 未发现架构违规问题
```

**说明**：git diff 中无 `A` 状态的 `.java` 文件，跳过检查。

### 场景 2：新增文件包含架构违规

```bash
$ git diff --name-status HEAD
A   src/main/java/com/example/api/NewApiReq.java
M   src/main/java/com/example/api/OrderRsp.java

$ /architecture-check
## 架构检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | api/NewApiReq.java | 3 | 接口层 import 基础设施层 OrderEntity | Entity 不可泄露到接口层，移除 import |
```

**说明**：
- `NewApiReq.java` 是新增文件（A），触发严格检查
- `OrderRsp.java` 是修改文件（M），不触发架构检查

### 场景 3：指定路径检查

```bash
$ /architecture-check src/main/java/com/example/infra
## 架构检查结果
✅ 未发现架构违规问题
```

**说明**：`infra` 目录下无新增文件，跳过检查。

### 场景 4：全面检查

```bash
$ /check
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

## 验证覆盖

| 场景 | 预期行为 | 验证结果 |
|------|----------|----------|
| 无新增文件 | 跳过检查 | ✅ 通过 |
| 新增文件有违规 | 报告 CRITICAL | ✅ 通过 |
| 修改文件不检查 | 不报告 | ✅ 通过 |
| 存量文件不检查 | 不报告 | ✅ 通过 |
| 指定路径无新增 | 跳过检查 | ✅ 通过 |

## 许可证

MIT