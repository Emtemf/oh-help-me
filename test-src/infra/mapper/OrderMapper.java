package com.example.infra.mapper;

public class OrderMapper {

    public String findOrderById(String id) {
        // SQL注入风险：使用 ${} 而不是 #{}
        String sql = "SELECT * FROM orders WHERE id = ${id}";
        return sql;
    }

    public void save() {
        // 硬编码密钥
        String password = "hardcoded_password_123";
        String apiKey = "sk-xxxxx-yyyyy-zzzzz";
    }
}