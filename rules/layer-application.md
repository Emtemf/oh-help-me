---
paths:
  - "**/application/**"
---

# 应用层规则

## 命名规范

- MUST: 应用服务命名为 `XxxApplicationService`，放在 `application/` 根目录
- MUST: 入参：简单场景直接拆字段，复杂场景用 `XxxDTO`
- MUST: 查询条件用 `XxxCondition`，放在 `application/condition/`
- MUST: 出参统一用 `XxxDTO`、`XxxDetailDTO`，放在 `application/dto/`
- MUST: MapStruct Mapper 放在 `application/convert/`（与 dto 同级）

## 应用服务职责

- MUST: 编排领域服务调用
- MUST: 处理事务边界
- MUST: 发送 MQ 消息
- MUST: 调用领域服务后，将 Model 转为 DTO 返回

```java
// application/OrderApplicationService.java
public class OrderApplicationService {
    private final OrderService orderService;
    private final MQProducer mqProducer;

    // 写操作
    public Long createOrder(Long userId, List<CreateOrderLineReq> lines) {
        // Req → Model（手写转换）
        List<OrderLine> orderLines = lines.stream()
            .map(l -> new OrderLine(l.getProductId(), l.getQuantity(), l.getPrice()))
            .toList();

        Order order = orderService.createOrder(userId, orderLines);

        // MQ 发送（应用层负责）
        mqProducer.send("order.created", new OrderMessage(order.getId()));

        return order.getId();
    }

    // 读操作
    public OrderDTO getOrder(Long id) {
        Order order = orderService.getOrder(id);
        return OrderDTO.from(order);  // MapStruct
    }

    // 条件查询
    public PageDTO<OrderListDTO> listOrders(OrderListCondition condition) {
        PageDTO<Order> page = orderService.listOrders(condition);
        return page.map(OrderListDTO::from);  // MapStruct
    }
}
```

## DTO 规范

- MUST: DTO 只在应用层，不传给领域层，不返回给接口层
- MUST: DTO 包含静态工厂方法 `from()`，内部调用 MapStruct Mapper
- MUST: DTO 字段根据接口需求定义，不必与 Model 一一对应

```java
// application/dto/OrderDTO.java
public class OrderDTO {
    private Long id;
    private String status;
    private BigDecimal totalAmount;

    public static OrderDTO from(Order order) {
        return OrderDTOMapper.INSTANCE.toDTO(order);
    }

    public static List<OrderDTO> fromList(List<Order> orders) {
        return OrderDTOMapper.INSTANCE.toDTOList(orders);
    }
}
```

## MapStruct Mapper

- MUST: 放在 `application/convert/` 目录（与 dto 同级）
- MUST: 使用 instance 模式（不依赖 Spring）
- MUST: 定义 `Model → DTO` 转换方法

```java
// application/convert/OrderDTOMapper.java
@Mapper
public interface OrderDTOMapper {
    OrderDTOMapper INSTANCE = Mappers.getMapper(OrderDTOMapper.class);

    OrderDTO toDTO(Order order);
    List<OrderDTO> toDTOList(List<Order> orders);
    OrderDetailDTO toDetailDTO(Order order);
}
```

## Condition 规范

- MUST: 用于查询条件封装
- MUST: 包含分页参数

```java
// application/condition/OrderListCondition.java
public class OrderListCondition {
    private Long userId;
    private String status;
    private int pageNum;
    private int pageSize;
}
```

## 入参规则

```java
// 简单场景（≤3 字段）：直接拆开传
public OrderDTO getOrder(Long orderId)
public void cancelOrder(Long orderId)
public void updateOrder(Long id, String address, String remark)

// 复杂场景：用 DTO 包装
public Long createOrder(CreateOrderDTO dto)
public PageDTO<OrderListDTO> listOrders(OrderListCondition condition)
```

## 依赖方向

- MUST: 应用层依赖领域层（调用 Service、Repository、Gateway）
- MUST: 应用层不依赖基础设施层
- MUST: 应用层不依赖接口层（Req/Rsp）

## 禁止

- MUST NOT: DTO 传给领域层
- MUST NOT: Model 直接返回给接口层
- MUST NOT: 应用层依赖 `infrastructure/` 下任何类
- MUST NOT: 应用层依赖 Req/Rsp（接口层对象）
- MUST NOT: 在应用层写 HTTP/数据库操作
