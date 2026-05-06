---
paths:
  - "**/interface/**"
---

# 接口层规则

## 目录结构

```
api/                              # 接口层（interface层）
├── OrderApiImpl.java             # 手写，实现 api-codegen 生成的接口
├── req/                          # api-codegen 生成，勿手动改
├── rsp/                          # api-codegen 生成，勿手动改
├── consumer/                     # MQ 消费者
│   └── OrderEventConsumer.java
└── scheduled/                    # 定时任务
    └── OrderScheduledJobs.java
```

## 命名规范

- MUST: 接口实现类命名为 `XxxApiImpl`，放在 `api/` 根目录
- MUST: 请求对象为 `XxxReq`，响应对象为 `XxxRsp`，由 api-codegen 生成
- MUST: MQ 消费者命名为 `XxxEventConsumer`，放在 `api/consumer/`
- MUST: 定时任务命名为 `XxxScheduledJobs`，放在 `api/scheduled/`

## Controller 规范

- MUST: 调用 ApplicationService，不调用 DomainService
- MUST: Req 拆字段传给 ApplicationService（简单场景）或构造 DTO（复杂场景）
- MUST: ApplicationService 返回 DTO 后，在 Controller 内转为 Rsp
- MUST: Rsp 转换使用私有方法，字段少直接赋值

```java
// api/OrderApiImpl.java
@Override
public R<OrderRsp> getOrder(Long id) {
    OrderDTO dto = orderService.getOrder(id);
    return R.ok(toRsp(dto));
}

@Override
public R<OrderRsp> createOrder(CreateOrderReq req) {
    Long orderId = orderService.createOrder(req.getUserId(), req.getLines());
    return R.ok(new OrderRsp(orderId));
}

@Override
public R<PageRsp<OrderListRsp>> listOrders(OrderListReq req) {
    OrderListCondition condition = new OrderListCondition(
        req.getUserId(),
        req.getStatus(),
        req.getPageNum(),
        req.getPageSize()
    );
    PageDTO<OrderListDTO> page = orderService.listOrders(condition);
    return R.ok(toPageRsp(page));
}

// Rsp 转换（私有方法）
private static OrderRsp toRsp(OrderDTO dto) {
    OrderRsp rsp = new OrderRsp();
    rsp.setId(dto.getId());
    rsp.setStatus(dto.getStatus().name());
    rsp.setTotalAmount(dto.getTotalAmount());
    return rsp;
}
```

## MQ 消费者规范

- MUST: 消费者只做消息解析 + 调用 ApplicationService
- MUST: 不在消费者内写业务逻辑

```java
// api/consumer/OrderEventConsumer.java
@Component
public class OrderEventConsumer {
    private final OrderApplicationService orderService;

    @RabbitListener(queues = "stock.deducted.queue")
    public void onStockDeducted(StockDeductedMessage msg) {
        orderService.confirmOrder(msg.getOrderId());
    }
}
```

## 定时任务规范

- MUST: 定时任务只做时间计算 + 调用 ApplicationService
- MUST: 不在定时任务内写业务逻辑

```java
// api/scheduled/OrderScheduledJobs.java
@Component
public class OrderScheduledJobs {
    private final OrderApplicationService orderService;

    @Scheduled(cron = "0 */5 * * * ?")
    public void cancelTimeoutOrders() {
        orderService.cancelTimeoutOrders(LocalDateTime.now().minusMinutes(30));
    }
}
```

## 对象转换规则

| 转换方向 | 方式 | 位置 |
|---------|------|-----|
| Req → 字段/DTO | 手写拆字段 | 接口层 Controller |
| Condition 构造 | 手写 | 接口层 Controller |
| DTO → Rsp | 手写赋值 | 接口层私有方法 |

## 禁止

- MUST NOT: Controller 直接调用 DomainService 或 Repository
- MUST NOT: Req/Rsp 传递到应用层或领域层
- MUST NOT: 在接口层写业务逻辑
- MUST NOT: 直接返回 Model/DTO 给前端（必须转 Rsp）
