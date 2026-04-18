package com.example.api;

// 正常的接口层请求对象
public class OrderReq {
    private String orderId;
    private String customerId;

    public String getOrderId() {
        return orderId;
    }

    public String getCustomerId() {
        return customerId;
    }
}