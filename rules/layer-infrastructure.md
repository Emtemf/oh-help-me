---
paths:
  - "**/infrastructure/**"
---

# 基础设施层规则

## 命名规范

- MUST: 数据库实体类带 `Entity` 后缀（如 `OrderEntity`、`OrderLineEntity`）
- MUST: 实体类放在 `infrastructure/entity/` 目录
- MUST: 仓储实现类命名为 `XxxRepositoryImpl`，放在 `infrastructure/repository/`
- MUST: MyBatis Mapper 放在 `infrastructure/mapper/`
- MUST: 外部请求/响应对象（如 `WechatPayRequest`）只在基础设施层内，不泄露

## 对象转换（核心）

- MUST: Mapper 返回 Entity，不直接返回领域对象
- MUST: 在 RepositoryImpl 中实现 `Entity → 领域对象` 转换
- MUST: 转换方法命名为 `toXxx()`（如 `toOrder()`、`toOrderLines()`）
- MUST: `save` 时实现 `领域对象 → Entity` 转换，命名为 `toEntity()`、`toLineEntity()`

### 读取转换模板

```java
@Override
public Order findById(Long id) {
    OrderEntity entity = orderMapper.selectById(id);
    if (entity != null) {
        Order order = toOrder(entity);
        // 关联查询子实体
        List<OrderLineEntity> lineEntities = lineMapper.selectByOrderId(id);
        order.setLines(toOrderLines(lineEntities));
        return order;
    }
    return null;
}

private Order toOrder(OrderEntity entity) {
    Order order = new Order();
    order.setId(entity.getId());
    order.setUserId(entity.getUserId());
    order.setStatus(OrderStatus.valueOf(entity.getStatus()));
    order.setTotalAmount(entity.getTotalAmount());
    return order;
}

private List<OrderLine> toOrderLines(List<OrderLineEntity> entities) {
    return entities.stream()
        .map(e -> new OrderLine(e.getProductId(), e.getQuantity(), e.getPrice()))
        .toList();
}
```

### 写入转换模板

```java
@Override
public void save(Order order) {
    OrderEntity entity = toEntity(order);
    orderMapper.insert(entity);
    for (OrderLine line : order.getLines()) {
        OrderLineEntity lineEntity = toLineEntity(line, entity.getId());
        lineMapper.insert(lineEntity);
    }
}

private OrderEntity toEntity(Order order) {
    OrderEntity entity = new OrderEntity();
    entity.setId(order.getId());
    entity.setUserId(order.getUserId());
    entity.setStatus(order.getStatus().name());
    entity.setTotalAmount(order.getTotalAmount());
    return entity;
}
```

## 缓存

- MUST: 缓存操作在 RepositoryImpl 内完成，对领域层透明
- MUST: 缓存 key 格式：`业务:标识`（如 `order:{id}`）
- MUST: 缓存命中直接返回领域对象，未命中则查库后回填

## 外部调用（Gateway 实现）

- MUST: 实现 `XxxGateway` 接口，命名为 `具体渠道 + Gateway`（如 `WechatPaymentGateway`）
- MUST: 领域对象 → 外部请求对象在 Gateway 实现内转换
- MUST: 外部响应 → 领域对象在 Gateway 实现内转换
- MUST: 外部请求/响应对象不出基础设施层

## 禁止

- MUST NOT: 领域层直接依赖 Entity
- MUST NOT: Entity 泄露到基础设施层之外（方法返回值、参数均不可）
- MUST NOT: Mapper 返回领域对象
- MUST NOT: 外部 API 对象泄露到领域层
