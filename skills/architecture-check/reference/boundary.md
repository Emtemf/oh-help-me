---
path: .
---

# 边界隔离规则

## 依赖方向（核心）

```
接口层 → 应用层 → 领域层 → 基础设施层
  ↓        ↓        ↓         ↓
 Req/Rsp   DTO     Model    Entity/Mapper
```

- MUST: 依赖只能从外向内（接口层 → 应用层 → 领域层 → 基础设施层）
- MUST NOT: 内层依赖外层（如领域层依赖应用层）

## 对象边界

| 对象 | 所在层 | 不可传递到 |
|-----|-------|----------|
| Req/Rsp | 接口层 | 应用层、领域层、基础设施层 |
| DTO/Condition | 应用层 | 领域层、基础设施层、接口层返回 |
| Model | 领域层 | 接口层返回、基础设施层存储 |
| Entity | 基础设施层 | 任何其他层 |
| 外部请求/响应 | 基础设施层 | 任何其他层 |

## 各层对象一览

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

## 常见错误对照

| 错误 | 问题 | 正确做法 |
|-----|------|---------|
| 应用层入参叫 `Param` | 无业务含义 | 用 DTO 或直接拆字段 |
| 领域层实体叫 `XxxEntity` | Entity 后缀属于基础设施层 | 领域层叫 `Xxx`，基础设施层叫 `XxxEntity` |
| 写 `OrderConverter.toDTO(order)` | 工具类无意义 | `OrderDTO.from(order)` + MapStruct |
| DTO 传给领域层 | 破坏隔离 | 应用层拆分字段 |
| Model 直接返回给接口层 | 破坏隔离 | 应用层转成 DTO |
| 外部 API 对象泄露到领域层 | 破坏隔离 | 基础设施层转换 |
| Mapper 直接返回领域对象 | 绕过 Entity 层 | Mapper 返回 Entity，基础设施层转为领域对象 |

## 检查清单

创建/修改文件时检查：

- [ ] 文件所在目录是否正确（如 Entity 在 `infrastructure/entity/`）
- [ ] 类命名是否符合规范（如领域层不带 Entity 后缀）
- [ ] import 是否违反依赖方向（如领域层 import 基础设施层）
- [ ] 方法参数/返回值是否违反对象边界
- [ ] 是否有对象跨层传递

## 端口/适配器模式（六边形架构）

- 端口：领域层定义的接口，表达"需要什么能力"
- 适配器：基础设施层的实现，表达"如何提供能力"

常见端口与适配器：

| 端口（领域层接口） | 适配器（基础设施层实现） | 外部服务 |
|------------------|------------------------|---------|
| `PaymentGateway` | `WechatPaymentGateway` | 支付 |
| `SmsGateway` | `AliyunSmsGateway` | 短信 |
| `OssGateway` | `AliyunOssGateway` | 存储 |
| `EmailGateway` | `SmtpEmailGateway` | 邮件 |
