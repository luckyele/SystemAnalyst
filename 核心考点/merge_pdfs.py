# -*- coding: utf-8 -*-
"""按章节顺序合并《系统分析师核心考点》PDF，并为每章添加书签。

用法：python merge_pdfs.py
依赖：pip install pypdf
"""
import os
from pypdf import PdfWriter

BASE = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "第0章 《系统分析师教程》第1~22章核心知识点总览.pdf",
    "第0章 系统分析师考试分析.pdf",
    "第1章 绪论核心知识点.pdf",
    "第2章 数学与工程基础核心考点.pdf",
    "第3章 计算机系统核心知识点.pdf",
    "第4章 计算机网络与分布式系统核心知识点.pdf",
    "第5章 数据库系统核心考点.pdf",
    "第6章 企业信息化核心知识点.pdf",
    "第7章 软件工程核心知识点.pdf",
    "第8章 项目管理的核心知识点总结.pdf",
    "第9章 信息安全核心知识点.pdf",
    "第10章 系统规划与分析核心知识点.pdf",
    "第11章 软件需求工程核心知识点.pdf",
    "第12章“软件架构设计”的核心知识点.pdf",
    "第13章 系统设计核心知识点.pdf",
    "第14章 软件实现与测试核心知识点.pdf",
    "第15章 系统运行与维护核心知识点.pdf",
    "第16章“Web应用系统分析与设计”的核心知识点.pdf",
    "第17章 嵌入式系统分析与设计核心知识点.pdf",
    "第18章「移动应用系统分析与设计」核心知识点.pdf",
    "第19章 大数据处理系统分析与设计核心知识点.pdf",
    "第20章 微服务系统分析与设计核心知识点.pdf",
    "第21章 信息物理系统（CPS）核心知识点.pdf",
    "第22章 论文写作要点知识点.pdf",
]

OUTPUT = "系统分析师核心考点（合并版）.pdf"

writer = PdfWriter()
page_count = 0
for name in FILES:
    path = os.path.join(BASE, name)
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    writer.append(path)  # append 会自动带入原书签
    writer.add_outline_item(os.path.splitext(name)[0], page_count)
    n = len(writer.pages) - page_count
    print(f"已合并: {name} ({n} 页)")
    page_count = len(writer.pages)

out_path = os.path.join(BASE, OUTPUT)
with open(out_path, "wb") as f:
    writer.write(f)

print(f"\n完成: {OUTPUT} 共 {page_count} 页")
