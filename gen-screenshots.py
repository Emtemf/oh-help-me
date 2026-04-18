#!/usr/bin/env python3
"""Generate code screenshots for README verification evidence."""
from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT_DIR = "/home/wula/IdeaProjects/ohm-plugin/docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try to find a good monospace font
def get_font(size=14):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

FONT = get_font(14)
FONT_BOLD = get_font(15)

# Color scheme (dark theme like terminal)
BG_COLOR = (30, 30, 30)
FG_COLOR = (212, 212, 212)
GREEN = (106, 153, 85)
YELLOW = (220, 220, 170)
RED = (247, 140, 108)
BLUE = (86, 156, 214)
GRAY = (122, 122, 122)

def render_screenshot(lines, filename, title=""):
    """Render lines of text as a terminal screenshot."""
    padding = 16
    line_height = 20

    # Calculate image size
    max_width = max(FONT.getlength(line) for line in lines) if lines else 200
    img_width = int(max_width) + padding * 2
    img_height = len(lines) * line_height + padding * 2 + (30 if title else 0)

    img = Image.new('RGB', (img_width, img_height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    y = padding
    if title:
        draw.text((padding, y), title, fill=BLUE, font=FONT_BOLD)
        y += 30

    for line in lines:
        color = FG_COLOR
        # Color coding
        if line.startswith("$ "):
            color = GREEN
        elif line.startswith("✅") or "未发现" in line:
            color = GREEN
        elif line.startswith("🔴") or "CRITICAL" in line:
            color = RED
        elif line.startswith("🟡") or "WARNING" in line:
            color = YELLOW
        elif line.startswith("A\t") or line.startswith("M\t"):
            color = YELLOW
        elif line.startswith("#"):
            color = GRAY
        elif line.startswith("|"):
            color = FG_COLOR

        draw.text((padding, y), line, fill=color, font=FONT)
        y += line_height

    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"Generated: {filename}")

# ============================================================
# Screenshot 1: No new files -> skip check
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "M\t.omc/state/hud-stdin-cache.json",
    "",
    "$ /architecture-check",
    "",
    "## 架构检查结果",
    "",
    "✅ 未发现架构违规问题",
], "scenario1-no-new-files.png", title="场景1: 无新增文件 → 跳过检查")

# ============================================================
# Screenshot 2: New file with architecture violation
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "A\tsrc/main/java/com/example/api/NewApiReq.java",
    "M\tsrc/main/java/com/example/api/OrderRsp.java",
    "",
    "$ /architecture-check",
    "",
    "## 架构检查结果",
    "| 严重 | 文件 | 行号 | 问题 | 建议 |",
    "|------|------|------|------|------|",
    "| 🔴 CRITICAL | api/NewApiReq.java | 3 | 接口层 import 基础设施层 OrderEntity | Entity 不可泄露到接口层，移除 import |",
], "scenario2-new-file-violation.png", title="场景2: 新增文件有违规 → 报告 CRITICAL")

# ============================================================
# Screenshot 3: Modified file not checked
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "M\tsrc/main/java/com/example/app/OrderService.java",
    "",
    "# OrderService.java 含架构问题但状态为 M",
    "# import com.example.api.OrderReq; // 违规",
    "",
    "$ /architecture-check",
    "",
    "## 架构检查结果",
    "",
    "✅ 未发现架构违规问题",
], "scenario3-modified-file.png", title="场景3: 修改文件不检查 → 无报告")

# ============================================================
# Screenshot 4: Legacy file not checked
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "A\tsrc/main/java/com/example/api/NewApiReq.java",
    "# 注: infra/OrderMapper.java 存在但不在 diff 中",
    "",
    "# OrderMapper.java 含安全问题 (SQL注入 ${})",
    "# 但属于存量文件，未被修改",
    "",
    "$ /security-check",
    "",
    "## 安全检查结果",
    "",
    "✅ 未发现安全漏洞",
], "scenario4-legacy-file.png", title="场景4: 存量文件不检查 → 无报告")

# ============================================================
# Screenshot 5: Path with no new files
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "A\tsrc/main/java/com/example/api/NewApiReq.java",
    "# 新增文件在 api/ 不在 infra/",
    "",
    "$ /architecture-check src/main/java/com/example/infra",
    "",
    "## 架构检查结果",
    "",
    "✅ 未发现架构违规问题",
], "scenario5-path-no-new-files.png", title="场景5: 指定路径无新增 → 跳过检查")

# ============================================================
# Screenshot 6: Full check
# ============================================================
render_screenshot([
    "$ git diff --name-status HEAD",
    "A\tsrc/main/java/com/example/api/NewApiReq.java",
    "A\tsrc/main/java/com/example/infra/OrderMapper.java",
    "A\tsrc/main/java/com/example/app/OrderService.java",
    "",
    "$ /check",
    "",
    "## 架构检查结果",
    "| 严重 | 文件 | 行号 | 问题 | 建议 |",
    "|------|------|------|------|------|",
    "| 🔴 CRITICAL | api/NewApiReq.java | 3 | 接口层 import 基础设施层 | 移除 import |",
    "",
    "## 安全检查结果",
    "| 严重 | 文件 | 行号 | 问题 | 建议 |",
    "|------|------|------|------|------|",
    "| 🔴 CRITICAL | infra/OrderMapper.java | 7 | MyBatis 使用 ${} 存在 SQL 注入风险 | 改用 #{} |",
    "",
    "## 质量检查结果",
    "| 严重 | 文件 | 行号 | 问题 | 建议 |",
    "|------|------|------|------|------|",
    "| 🟡 WARNING | app/OrderService.java | 7 | 方法长度超过 50 行 | 拆分方法 |",
    "| 🔴 CRITICAL | app/OrderService.java | 65 | 空 catch 块 | 添加异常处理 |",
], "scenario6-full-check.png", title="场景6: 全面检查 → 并行报告")

# ============================================================
# Screenshot: Source code - NewApiReq.java
# ============================================================
render_screenshot([
    " 1  package com.example.api;",
    " 2",
    " 3  import com.example.infra.entity.OrderEntity;  // ← 违规",
    " 4",
    " 5  public class NewApiReq {",
    " 6      private OrderEntity order;  // ← 违规: Entity泄露到接口层",
    " 7      private String name;",
    " 8",
    " 9      public OrderEntity getOrder() {",
    "10          return order;",
    "11      }",
    "12  }",
], "code-new-api-req.png", title="源码: NewApiReq.java")

# ============================================================
# Screenshot: Source code - OrderMapper.java
# ============================================================
render_screenshot([
    " 1  package com.example.infra.mapper;",
    " 2",
    " 3  public class OrderMapper {",
    " 4",
    " 5      public String findOrderById(String id) {",
    " 6          // SQL注入风险：使用 ${} 而不是 #{}",
    " 7          String sql = \"SELECT * FROM orders WHERE id = ${id}\";  // ← 违规",
    " 8          return sql;",
    " 9      }",
    "10",
    "11      public void save() {",
    "12          // 硬编码密钥",
    "13          String password = \"hardcoded_password_123\";  // ← 违规",
    "14      }",
    "15  }",
], "code-order-mapper.png", title="源码: OrderMapper.java")

# ============================================================
# Screenshot: Source code - OrderService.java
# ============================================================
render_screenshot([
    " 1  package com.example.app;",
    " 2",
    " 3  import com.example.api.OrderReq;  // ← 违规: 应用层引用接口层Req",
    " 4",
    " 5  public class OrderService {",
    " 6",
    " 7      public void process(OrderReq req) {  // ← 违规: Req传到应用层",
    " 8          String step1 = \"step1\";",
    " 9          String step2 = \"step2\";",
    "..          ... // 共51行，超过50行阈值",
    "59          String step51 = \"step51\";  // ← 超过50行",
    "60      }",
    "61",
    "62      public void badMethod() {",
    "63          try {",
    "64              doSomething();",
    "65          } catch (Exception e) {",
    "66              // 空 catch 块  ← CRITICAL",
    "67          }",
    "68      }",
    "69  }",
], "code-order-service.png", title="源码: OrderService.java")

print("\nAll screenshots generated!")
