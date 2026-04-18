package com.example.domain;

import com.example.infra.entity.OrderEntity; // 违规：领域层引用基础设施层

public class Order {
    private Long id;
    private OrderEntity entity; // 违规：Entity泄露到领域层
}