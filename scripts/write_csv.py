#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
三菱 FX5U PLC CSV 文件写入工具

用法 1：命令行传 JSON
  echo '[["0","","LDP","X0","","",""],["2","","SET","M0","","",""]]' | python write_csv.py ProgPou_test

用法 2：Python 模块导入
  from write_csv import write_plc_csv
  rows = [["0", "", "LDP", "X0", "", "", ""], ...]
  write_plc_csv(rows, "C:/Users/admin/Desktop/ProgPou_test.csv")
"""

import codecs
import json
import sys
import os


def write_plc_csv(rows, output_path):
    """
    将 PLC 程序行写入 UTF-16LE CSV 文件（GX Works3 扩展格式）

    rows: 列表的列表，每行 7 列: [步号, 行间声明, 指令, I/O软元件, 空白栏, PI声明, 注解]
    output_path: 输出文件路径（绝对路径）
    """
    # 确保输出目录存在
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    with open(output_path, 'wb') as f:
        # UTF-16LE BOM
        f.write(b'\xff\xfe')

        content = []

        # 文件头 3 行
        content.append('"(工程未设置)"\r\n')
        content.append('"机型信息:"\t"FX5CPU FX5U"\r\n')
        content.append(
            '"步号"\t"行间声明"\t"指令"\t"I/O(软元件)"\t"空白栏"\t"PI声明"\t"注解"\r\n'
        )

        # 数据行
        for row in rows:
            # 确保每行正好 7 列
            padded = list(row) + [''] * (7 - len(row))
            line = '\t'.join(f'"{col}"' for col in padded)
            content.append(line + '\r\n')

        # 编码为 UTF-16LE 写入
        for line in content:
            f.write(line.encode('utf-16-le'))


def generate_script_rows(rows, program_name, description="", output_dir=None):
    """
    生成一个完整的独立 Python 脚本，包含 rows 数据和编码逻辑。

    rows: 程序行列表
    program_name: 程序名（不含路径），如 "motor_interlock"
    description: 程序功能描述
    output_dir: 输出目录，默认桌面

    返回：生成的 Python 脚本内容字符串
    """
    if output_dir is None:
        output_dir = "C:/Users/admin/Desktop"

    output_path = f"{output_dir}/ProgPou_{program_name}.csv"

    script = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLC 程序：{description}
输出文件：{output_path}
"""
import codecs
import os

rows = {repr(rows)}

output_path = {repr(output_path)}

with open(output_path, 'wb') as f:
    f.write(b'\\xff\\xfe')

    content = []
    content.append('"(工程未设置)"\\r\\n')
    content.append('"机型信息:"\\t"FX5CPU FX5U"\\r\\n')
    content.append('"步号"\\t"行间声明"\\t"指令"\\t"I/O(软元件)"\\t"空白栏"\\t"PI声明"\\t"注解"\\r\\n')

    for row in rows:
        padded = list(row) + [''] * (7 - len(row))
        line = '\\t'.join(f'"{{col}}"' for col in padded)
        content.append(line + '\\r\\n')

    for line in content:
        f.write(line.encode('utf-16-le'))

print(f"文件已创建: {{output_path}}")
'''
    return script


def validate_rows(rows):
    """验证程序行的基本正确性"""
    issues = []

    if not rows:
        issues.append("程序行为空")
        return issues

    # 检查最后一行是否为 END
    last_row = rows[-1]
    last_instr = last_row[2] if len(last_row) > 2 else ""
    if last_instr != "END":
        issues.append("程序最后一行必须是 END 指令")

    # 检查步号
    seen_steps = set()
    for i, row in enumerate(rows):
        step = row[0] if len(row) > 0 else ""
        if step != "":
            if step in seen_steps:
                issues.append(f"步号 {step} 重复（第 {i+1} 行）")
            seen_steps.add(step)

    return issues


# 命令行入口
if __name__ == "__main__":
    if len(sys.argv) > 1:
        program_name = sys.argv[1]
    else:
        program_name = "program"

    output_dir = sys.argv[2] if len(sys.argv) > 2 else "C:/Users/admin/Desktop"
    output_path = f"{output_dir}/ProgPou_{program_name}.csv"

    # 从标准输入读取 JSON
    data = sys.stdin.read()
    rows = json.loads(data)

    issues = validate_rows(rows)
    if issues:
        print("警告：")
        for issue in issues:
            print(f"  - {issue}")
        print()

    write_plc_csv(rows, output_path)
    print(f"文件已创建: {output_path}")
    print(f"编码: UTF-16LE with BOM")
    print(f"程序行数: {len(rows)}")
