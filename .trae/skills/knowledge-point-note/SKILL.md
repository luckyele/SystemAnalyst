---
name: knowledge-point-note
description: Turn a finished concept explanation into a numbered note plus a rendered diagram PNG under 知识点位. Use when the user says 保存到知识点位, 存成知识点, or asks to save an answer with its images.
---

# 知识点位笔记

把一个已经讲清楚的考点，落成 `知识点位/` 下的编号 Markdown 与同名配图。

## 步骤

### 1. 定编号与文件名

- 列出 `知识点位/`，取现有最大编号加一，两位补零。
- 文件名格式 `NN-主题.md`。主题用中文短名，不含空格，多关键词之间用连字符。
- 配图与笔记同名、同目录：`NN-主题.png`，不建子目录。

### 2. 写正文

- 一级标题 `# 主题`；二级标题用 `## 一、` `## 二、` 中文序号。
- 段落顺序固定：概念与机制 → 成立前提 → 对比或计算 → 失效场景与辨析 → 小结。
- 并列项用表格；公式单独放进 fenced code block，便于复制。
- 句子要短，一句一个意思。能落到具体数字就写数字，不写「显著提升」「大幅优化」这类空话。
- 收尾写一段可背诵的短结论，不超过三句。

### 3. 画图

- 复制 `assets/diagram-template.svg` 再改内容。保持 720×430 画布、四周至少 40 的安全边距、CSS 变量块与明暗两套取值。
- 只画机制本身，不画「关于机制的说明」。一个焦点用品牌色；只有故障、异常、危险状态才用语义红。
- 正文里用 `![图注](NN-主题.png)` 引用，图注写清这张图画的是什么。

### 4. 渲染 PNG

- 运行 `scripts/render-svg.sh 图.svg 知识点位/NN-主题.png`，默认输出 2 倍分辨率。
- 用 Read 打开 PNG 目视检查：文字不重叠、不被截断，箭头没被画布裁掉。不合格就改 SVG 重渲，不要交付没看过的图。

### 5. 校验

- 运行 `python3 tools/check-md.py 知识点位/NN-主题.md`。
- 确认正文图片路径与磁盘上的文件名逐字一致。

## 边界

- 只整理已经讲透的内容，不边写边补资料。
- 不新建 `images/` 子目录，不套用 `Pasted image` 命名。
- 用户没要求时，不额外生成 PDF。
