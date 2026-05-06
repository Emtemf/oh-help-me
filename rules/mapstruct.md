---
paths:
  - "**/application/convert/**"
---

# MapStruct 规则

## 使用模式

- MUST: 使用 instance 模式（`Mappers.getMapper()`），不使用 Spring 模式
- MUST: MapStruct Mapper 放在 `application/convert/` 目录（与 `dto/` 同级）
- MUST: 只定义 `Model → DTO` 转换，不定义反向

## 转换方向一览

| 转换方向 | 方式 | 位置 | 说明 |
|---------|------|-----|------|
| Req → 字段/DTO | 接口层拆分 | 接口层 Controller | Req 是生成的，拆字段即可 |
| Condition 构造 | 接口层拆分 | 接口层 Controller | 简单构造 |
| Model → DTO | MapStruct + default | 应用层 convert/ | 自动映射 + default 方法处理复杂逻辑 |
| DTO → Rsp | 接口层拆分 | 接口层私有方法 | Rsp 是生成的，字段少直接赋值 |
| Entity → Model | MapStruct + default | 基础设施层 RepositoryImpl | 基础设施层内转换 |
| Model → Entity | MapStruct + default | 基础设施层 RepositoryImpl | save 时转换 |
| 外部响应 → 领域对象 | MapStruct + default | 基础设施层 GatewayImpl | 外部对象不出基础设施层 |

## MapStruct Mapper 模板

```java
// application/convert/OrderDTOMapper.java
@Mapper
public interface OrderDTOMapper {
    OrderDTOMapper INSTANCE = Mappers.getMapper(OrderDTOMapper.class);

    // 简单字段自动映射
    OrderDTO toDTO(Order order);
    List<OrderDTO> toDTOList(List<Order> orders);
    OrderDetailDTO toDetailDTO(Order order);

    // 复杂逻辑用 default 方法处理
    default String formatStatus(Order order) {
        return "状态：" + order.getStatus().getDesc();
    }

    default BigDecimal calculateDiscount(Order order) {
        if (order.getTotalAmount().compareTo(BigDecimal.valueOf(1000)) > 0) {
            return order.getTotalAmount().multiply(BigDecimal.valueOf(0.9));
        }
        return order.getTotalAmount();
    }
}
```

## DTO 静态工厂方法模板

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

## 调用方式

- MUST: 应用层通过 `XxxDTO.from(model)` 调用，不直接调用 Mapper
- MUST: 列表转换用 `page.map(XxxDTO::from)` 或 `XxxDTO.fromList(list)`

## 为什么转换器在应用层而非基础设施层

- 依赖方向：`Model → DTO` 依赖 DTO（应用层对象），放基础设施层会反向依赖
- 职责清晰：基础设施层只负责 `外部响应 → 领域对象` 和 `Entity ↔ Model`
- 测试便利：应用层转换器可纯单元测试

## 迁移策略（BeanUtils → MapStruct）

1. 标记旧 Converter `@Deprecated`
2. 在 `convert/` 下新建 MapStruct Mapper
3. 复杂逻辑用 `default` 方法实现
4. 全局搜索 `XxxConverter.to`，替换为 `XxxDTO.from`
5. 确认无调用后，删除 `converter/` 下的文件

## 禁止

- MUST NOT: 使用 Spring 模式（`componentModel = "spring"`）
- MUST NOT: 使用 BeanUtils.copyProperties（新代码）
- MUST NOT: 写 `XxxConverter.toDTO(order)` 工具类（用 `XxxDTO.from()`）
- MUST NOT: 在基础设施层定义 `Model → DTO` 转换
- MUST NOT: 手写转换类，复杂逻辑用 MapStruct default 方法
