---
paths:
  - "**/domain/**"
---

# 领域层规则

## 命名规范

- MUST: 领域对象不带 `Entity` 后缀（如 `Order`、`User`、`OrderLine`）
- MUST: 领域对象放在 `domain/model/` 目录
- MUST: 领域服务命名为 `XxxService`，放在 `domain/service/`
- MUST: 仓储接口命名为 `XxxRepository`，放在 `domain/repository/`
- MUST: 外部端口接口命名为 `XxxGateway`，放在 `domain/gateway/`

## 领域对象（Model）

- MUST: 领域对象是纯 POJO，不依赖任何框架
- MUST: 包含业务状态字段和行为方法
- MUST: 枚举类型放在 `domain/model/` 下

```java
// domain/model/Order.java
public class Order {
    private Long id;
    private Long userId;
    private List<OrderLine> lines;
    private OrderStatus status;
    private BigDecimal totalAmount;

    // 业务行为
    public void cancel() {
        if (status == OrderStatus.CREATED) {
            this.status = OrderStatus.CANCELLED;
        }
    }

    public void confirm() {
        if (status == OrderStatus.CREATED) {
            this.status = OrderStatus.CONFIRMED;
        }
    }
}
```

## 领域服务

- MUST: 封装业务规则和跨对象操作
- MUST: 依赖 Repository 接口，不依赖实现
- MUST: 依赖 Gateway 接口调用外部服务

```java
// domain/service/OrderService.java
public class OrderService {
    private final OrderRepository orderRepo;
    private final PaymentGateway paymentGateway;

    public Order createOrder(Long userId, List<OrderLine> lines) {
        Order order = new Order();
        order.setUserId(userId);
        order.setLines(lines);
        order.setStatus(OrderStatus.CREATED);
        order.setTotalAmount(calculateTotal(lines));
        orderRepo.save(order);
        return order;
    }

    public PaymentResult payOrder(Long orderId) {
        Order order = orderRepo.findById(orderId);
        PaymentResult result = paymentGateway.pay(orderId, order.getTotalAmount());
        order.setStatus(OrderStatus.PAID);
        order.setTradeNo(result.getTradeNo());
        orderRepo.save(order);
        return result;
    }
}
```

## 仓储接口（Repository）

- MUST: 只定义数据访问方法，不包含实现
- MUST: 返回领域对象，不返回 Entity
- MUST: 方法命名：`findById`、`save`、`findByCondition`、`delete` 等

```java
// domain/repository/OrderRepository.java
public interface OrderRepository {
    Order findById(Long id);
    void save(Order order);
    PageDTO<Order> findByCondition(OrderListCondition condition);
    void delete(Long id);
}
```

## 外部端口接口（Gateway）

- MUST: 定义外部能力接口，表达"需要什么能力"
- MUST: 返回领域对象或值对象，不返回外部 API 响应
- MUST: 参数使用基本类型或领域对象

```java
// domain/gateway/PaymentGateway.java
public interface PaymentGateway {
    PaymentResult pay(Long orderId, BigDecimal amount);
}

// domain/gateway/SmsGateway.java
public interface SmsGateway {
    void send(String phone, String content);
}
```

## 依赖方向

- MUST: 领域层不依赖基础设施层
- MUST: 领域层不依赖应用层
- MUST: 领域层不依赖接口层
- MUST: 通过接口（Repository、Gateway）声明依赖，由基础设施层实现

## 禁止

- MUST NOT: 领域对象带 `Entity` 后缀
- MUST NOT: 领域层依赖 `infrastructure/` 下任何类
- MUST NOT: 领域层依赖 DTO、Req、Rsp
- MUST NOT: 在领域层直接调用 HTTP/数据库/缓存
- MUST NOT: 外部 API 对象（Request/Response）出现在领域层
