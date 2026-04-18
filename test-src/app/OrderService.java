package com.example.app;

import com.example.api.OrderReq; // 违规：应用层引用接口层Req

public class OrderService {

    public void process(OrderReq req) { // 违规：Req传递到应用层
        // 方法超过50行演示
        String step1 = "step1";
        String step2 = "step2";
        String step3 = "step3";
        String step4 = "step4";
        String step5 = "step5";
        String step6 = "step6";
        String step7 = "step7";
        String step8 = "step8";
        String step9 = "step9";
        String step10 = "step10";
        String step11 = "step11";
        String step12 = "step12";
        String step13 = "step13";
        String step14 = "step14";
        String step15 = "step15";
        String step16 = "step16";
        String step17 = "step17";
        String step18 = "step18";
        String step19 = "step19";
        String step20 = "step20";
        String step21 = "step21";
        String step22 = "step22";
        String step23 = "step23";
        String step24 = "step24";
        String step25 = "step25";
        String step26 = "step26";
        String step27 = "step27";
        String step28 = "step28";
        String step29 = "step29";
        String step30 = "step30";
        String step31 = "step31";
        String step32 = "step32";
        String step33 = "step33";
        String step34 = "step34";
        String step35 = "step35";
        String step36 = "step36";
        String step37 = "step37";
        String step38 = "step38";
        String step39 = "step39";
        String step40 = "step40";
        String step41 = "step41";
        String step42 = "step42";
        String step43 = "step43";
        String step44 = "step44";
        String step45 = "step45";
        String step46 = "step46";
        String step47 = "step47";
        String step48 = "step48";
        String step49 = "step49";
        String step50 = "step50";
        String step51 = "step51"; // 超过50行
    }

    public void badMethod() {
        try {
            doSomething();
        } catch (Exception e) {
            // 空 catch 块 - CRITICAL
        }
    }

    private void doSomething() {}
}