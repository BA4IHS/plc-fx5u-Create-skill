# 三菱 FX5U PLC 程序生成器

根据语言描述的控制需求，自动生成符合 **GX Works3** 导入规范的 PLC 程序 CSV 文件。

## 安装

### 方式一：用 AI 工具一键安装

复制以下命令发给你的 AI 编程助手（Claude Code / OpenClaw / Hermes 等均可）：

> 帮我安装这个 skill：https://github.com/BA4IHS/plc-fx5u-Create-skill

AI 助手会自动克隆仓库并安装到 skill 目录。

### 方式二：Git 克隆（Claude Code）

```bash
git clone https://github.com/BA4IHS/plc-fx5u-Create-skill.git ~/.claude/skills/plc-fx5u-generator
```

### 方式三：下载文件手动放入

1. 下载本仓库 ZIP 并解压
2. 将解压后的文件夹重命名为 `plc-fx5u-generator`
3. 放入 Claude Code 的 skills 目录：
   - Windows：`%USERPROFILE%\.claude\skills\`
   - macOS / Linux：`~/.claude/skills/`

安装后在对话中直接描述 PLC 控制需求即可触发。

---

## 快速体验

在 AI 助手中输入：

> 生成一个 FX5U PLC 程序：按下启动按钮 X0，电机 Y0 运行 5 秒后停止 3 秒，如此循环。急停 X1 立即停止。

Skill 会自动分析需求、分配软元件、生成 Python 脚本和 CSV 文件，输出到桌面。

---

## 功能

| 能力 | 说明 |
|------|------|
| 需求理解 | 自动识别启停、互锁、定时、闪烁、循环、限位、急停等控制逻辑 |
| 软元件分配 | 自动规划 X/Y/M/T/C/F/D 地址 |
| CSV 生成 | UTF-16LE with BOM，Tab 分隔，双引号包围，可直接导入 GX Works3 |
| 扩展格式 | 定时器/计数器参数独立行，步号为空 |
| Python 脚本 | 同步生成可复现的 Python 脚本 |

## 支持的控制场景

- 电机启停与自锁保持
- 正反转互锁控制
- 定时循环运行
- 点动与长运行互锁
- 故障报警（闪烁 → 常亮 → 熄灭）
- 限位保护与自动循环
- 抢答器控制
- 送料小车 / 电梯等复杂流程

## CSV 格式规范

| 项目 | 规范 |
|------|------|
| 编码 | UTF-16LE with BOM |
| 分隔符 | 制表符 (Tab) |
| 列包围 | 双引号 |
| 7 列结构 | 步号、行间声明、指令、I/O(软元件)、空白栏、PI声明、注解 |
| 步号规则 | 偶数递增，参数行留空 |
| 定时器时基 | 100ms（K值 = 秒数 × 10） |
| 注解列 | **必须为空**（填入文本会导致 GX Works3 导入报错） |

## 文件结构

```
plc-fx5u-generator/
├── SKILL.md                          # Skill 主文件
├── references/
│   ├── csv-format-spec.md            # CSV 格式详细规范
│   ├── instruction-set.md            # FX5U 指令参考（LD/SET/RST/OUT/ANI/PLS/FF...）
│   └── program-examples.md           # 典型程序示例（电机、报警、小车、互锁）
└── scripts/
    └── write_csv.py                  # CSV 写入工具（可独立使用）
```

## 注意事项

- 注解列（第 7 列）必须为空，否则 GX Works3 导入报错
- 急停逻辑必须复位所有输出和中间继电器及定时器
- 正反转 / 上下行必须硬件互锁（ANI Yx）
- 输出文件默认保存到 `C:/Users/admin/Desktop/`
- 生成后请用 GX Works3 验证程序逻辑后再下载到 PLC
