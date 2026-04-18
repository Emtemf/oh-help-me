package com.example.api;

import com.example.infra.entity.OrderEntity; // 违规：接口层引用基础设施层

public class NewApiReq {
    private OrderEntity order; // 违规：Entity泄露到接口层
    private String name;

    public OrderEntity getOrder() {
        return order;
    }
}