# 架构检查规则参考

## 边界隔离规则

### 依赖方向（核心）

```
接口层 → 应用层 → 领域层 → 基础设施层
  ↓        ↓        ↓         ↓
 Req/Rsp   DTO     Model    Entity/Mapper
```

- MUST: 依赖只能从外向内（接口层 → 应用层 → 领域层 → 基础设施层）
- MUST NOT: 内层依赖外层（如领域层依赖应用层）

### 对象边界

| 对象 | 所在层 | 不可传递到 |
|-----|-------|----------|
| Req/Rsp | 接口层 | 应用层、领域层、基础设施层 |
| DTO/Condition | 应用层 | 领域层、基础设施层、接口层返回 |
| Model | 领域层 | 接口层返回、基础设施层存储 |
| Entity | 基础设施层 | 任何其他层 |
| 外部请求/响应 | 基础设施层 | 任何其他层 |

### 各层对象一览

| 层 | 对象类型 | 命名示例 | 说明 |
|---|---|---|---|
| 接口层 | 请求 | `CreateOrderReq` | api-codegen 生成 |
| 接口层 | 响应 | `OrderRsp` | api-codegen 生成 |
| 应用层 | 写入参 | `CreateOrderDTO` | 复杂场景用 |
| 应用层 | 查入参 | `OrderListCondition` | 条件查询 |
| 应用层 | 出参 | `OrderDTO` | 统一叫 DTO |
| 领域层 | 实体 | `Order` | 不带 Entity 后缀 |
| 领域层 | 服务 | `OrderService` | 领域服务 |
| 领域层 | 仓储接口 | `OrderRepository` | 数据访问接口 |
| 领域层 | 外部端口 | `PaymentGateway` | 外部调用接口 |
| 基础设施层 | 实体 | `OrderEntity` | 带 Entity 后缀 |
| 基础设施层 | 仓储实现 | `OrderRepositoryImpl` | 实现领域层接口 |
| 基础设施层 | Mapper | `OrderMapper` | MyBatis |

### 常见错误对照

| 错误 | 问题 | 正确做法 |
|-----|------|---------|
| 应用层入参叫 `Param` | 无业务含义 | 用 DTO 或直接拆字段 |
| 领域层实体叫 `XxxEntity` | Entity 后缀属于基础设施层 | 领域层叫 `Xxx`，基础设施层叫 `XxxEntity` |
| DTO 传给领域层 | 破坏隔离 | 应用层拆分字段 |
| Model 直接返回给接口层 | 破坏隔离 | 应用层转成 DTO |
| 外部 API 对象泄露到领域层 | 破坏隔离 | 基础设施层转换 |
| Mapper 直接返回领域对象 | 绕过 Entity 层 | Mapper 返回 Entity，基础设施层转为领域对象 |

## 存量代码规则

### 核心原则

- MUST: 新建文件严格遵循规范
- MUST: 修改已有文件时，只改用户要求的部分，不扩散
- MUST NOT: 不主动改用户没要求改的东西

### 判断方式：git diff

| git diff 状态 | 含义 | 行为 |
|-------------|------|-----|
| `A` (Added) | 新建文件 | 严格遵循规范 |
| `M` (Modified) | 修改已有文件 | 不检查架构违规 |
| 不在 diff 里 | 存量文件未动 | 不检查 |

### 禁止

- MUST NOT: 顺手改、顺便改、建议改用户没要求改的代码
- MUST NOT: 在 code review 中对存量文件提规范建议（除非用户问）
- MUST NOT: 批量重命名、批量迁移、批量重构存量代码
