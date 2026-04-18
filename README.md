# ohm - oh-help-me

A Claude Code plugin for Java code review workflow with Clean Architecture checks.

## Installation

```bash
# Install from GitHub marketplace (coming soon)
/plugin install ohm

# Or install locally from directory
/plugin install /path/to/ohm-plugin
```

## Features

### Skills

#### `architecture-check`
Check Clean Architecture compliance:
- Dependency direction violations (domain layer importing infrastructure layer)
- Object boundary violations (Entity leaking outside infrastructure layer)

```bash
# Check git diff changes only (new files)
/architecture-check

# Check specific path
/architecture-check src/main/java
```

#### `security-check`
Check Java security issues:
- SQL injection (MyBatis `${}`)
- Hardcoded secrets
- Unsafe deserialization

```bash
/security-check
```

#### `quality-check`
Check code quality:
- Method length > 50 lines
- Empty catch blocks
- printStackTrace usage

```bash
/quality-check
```

### Command

#### `check`
Run all checks in parallel:

```bash
/check              # Check git diff changes
/check src/main/    # Check specific path
```

## Design Principles

### Incremental Checking

Following `.claude/rules/clean-architecture/legacy-code.md`:

| git diff status | Behavior |
|-----------------|----------|
| `A` (Added) | Strict checking |
| `M` (Modified) | Skip architecture checks |
| Not in diff | Skip all checks |

**Only check new code, respect legacy code.**

### Subagent Isolation

Each skill runs in an isolated subagent session:
- `context: fork` - Isolated execution context
- `agent: Explore` - Uses Explore agent for code scanning

## Output Format

```
## 检查结果
| 严重 | 文件 | 行号 | 问题 | 建议 |
|------|------|------|------|------|
| 🔴 CRITICAL | domain/Order.java | 3 | 领域层 import 基础设施层 | 移除 import |
| 🟡 WARNING | app/OrderService.java | 52 | 方法长度超过 50 行 | 拆分方法 |
```

- 🔴 CRITICAL - Must fix before commit
- 🟡 WARNING - Should fix
- 🔵 SUGGESTION - Nice to have

## Configuration

Plugin respects project-level `.claude/rules/clean-architecture/` rules:

- `boundary.md` - Layer boundaries
- `legacy-code.md` - Incremental checking policy
- `layer-*.md` - Layer-specific rules

## License

MIT
