#!/usr/bin/env python3
"""Markdown 检查工具。

两部分：
  1. 自定义规则 MD-CJK-BOLD —— 检测 CommonMark 加粗（强调）定界符 `**` 的
     flanking 错误。中文写作里常见的 `**内容（全角标点）**汉字`，结束 `**`
     前是 Unicode 标点、后是汉字，不满足 right-flanking，`**` 不会闭合、会
     原样显示。此项为硬失败。
  2. 通用 lint —— 调用 pymarkdown（markdownlint 的 Python 移植版），
     默认仅提示，加 --strict 才计入失败。

用法：
    python3 tools/check-md.py                  # 扫描本目录全部 .md
    python3 tools/check-md.py 某个文件.md ...   # 只扫描指定文件/目录
    python3 tools/check-md.py --strict         # 通用 lint 也计入失败
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / ".pymarkdown.json"
PYMARKDOWN = ROOT / ".venv" / "bin" / "pymarkdown"

RULE_ID = "MD-CJK-BOLD"
MD_EXTENSIONS = {".md", ".markdown"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "dist", "build"}

FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
CODE_SPAN_RE = re.compile(r"(`+)(.+?)\1")
STAR_RUN_RE = re.compile(r"\*+")


def is_ws(ch: str) -> bool:
    """CommonMark 的 Unicode 空白：Z* 类别 + 制表/换行/换页/回车。"""
    return ch in " \t\n\f\r" or unicodedata.category(ch) == "Zs"


def is_punct(ch: str) -> bool:
    """CommonMark 的 Unicode 标点：类别 P*（Pc/Pd/Pe/Pf/Pi/Po/Ps）。"""
    return unicodedata.category(ch)[0] == "P"


def left_flanking(text: str, s: int, e: int) -> bool:
    """开头定界符 run [s, e) 是否 left-flanking。"""
    prev = text[s - 1] if s > 0 else " "
    nxt = text[e] if e < len(text) else " "
    if is_ws(nxt):
        return False
    if is_punct(nxt) and not (is_ws(prev) or is_punct(prev)):
        return False
    return True


def right_flanking(text: str, s: int, e: int) -> bool:
    """结束定界符 run [s, e) 是否 right-flanking。"""
    prev = text[s - 1] if s > 0 else " "
    nxt = text[e] if e < len(text) else " "
    if is_ws(prev):
        return False
    if is_punct(prev) and not (is_ws(nxt) or is_punct(nxt)):
        return False
    return True


def mask_code_spans(line: str) -> str:
    """把行内代码 span 掩码成等长字母，避免其中的 * 被误判为强调定界符。"""
    return CODE_SPAN_RE.sub(lambda m: "A" * len(m.group(0)), line)


def find_delimiters(masked: str) -> list[tuple[int, int]]:
    """返回该行所有「长度恰为 2」的 * run 的 (start, end)。"""
    return [
        (m.start(), m.end())
        for m in STAR_RUN_RE.finditer(masked)
        if m.end() - m.start() == 2
    ]


def scan_line(masked: str) -> list[tuple[int, str, str, str]]:
    """返回该行问题列表：(列号0基, kind, prev_char, next_char)。"""
    delims = find_delimiters(masked)
    findings: list[tuple[int, str, str, str]] = []

    for i in range(0, len(delims) - 1, 2):
        (os_, oe) = delims[i]
        (cs, ce) = delims[i + 1]
        if not left_flanking(masked, os_, oe):
            findings.append((os_, "opener", masked[os_ - 1] if os_ > 0 else "", masked[oe] if oe < len(masked) else ""))
        if not right_flanking(masked, cs, ce):
            findings.append((cs, "closer", masked[cs - 1] if cs > 0 else "", masked[ce] if ce < len(masked) else ""))

    if len(delims) % 2 == 1:
        s, e = delims[-1]
        findings.append((s, "unpaired", masked[s - 1] if s > 0 else "", masked[e] if e < len(masked) else ""))

    return findings


def iter_md_files(paths: list[str]):
    seen: set[Path] = set()
    for raw in paths:
        p = Path(raw)
        if p.is_file() and p.suffix.lower() in MD_EXTENSIONS:
            candidates = [p]
        elif p.is_dir():
            candidates = sorted(
                q for q in p.rglob("*") if q.is_file() and q.suffix.lower() in MD_EXTENSIONS
            )
        else:
            continue
        for q in candidates:
            if any(part in SKIP_DIRS for part in q.parts):
                continue
            rp = q.resolve()
            if rp not in seen:
                seen.add(rp)
                yield q


def scan_file(path: Path) -> int:
    """扫描单个文件，打印命中，返回问题数。"""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        print(f"{path}: 无法读取: {exc}", file=sys.stderr)
        return 0

    count = 0
    in_fence = False
    for lineno, raw in enumerate(lines, start=1):
        if FENCE_RE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for col, kind, prev, nxt in scan_line(mask_code_spans(raw)):
            count += 1
            print(f"{path}:{lineno}:{col + 1}: {RULE_ID} [{kind}]")
            if kind == "closer":
                print(f"    结束 ** 前是「{prev}」、后是「{nxt}」，不满足 right-flanking")
                print("    修复：在结束 ** 后补一个空格，或把标点移出 ** 之外")
            elif kind == "opener":
                print(f"    开头 ** 前是「{prev}」、后是「{nxt}」，不满足 left-flanking")
                print("    修复：在开头 ** 前补空格，或调整标点位置")
            else:
                print("    本行长度恰为 2 的 ** 数量为奇数，可能有未闭合的加粗")
            print(f"    原文：{raw.strip()}")
    return count


def run_pymarkdown(files: list[Path]) -> int | None:
    if not PYMARKDOWN.exists():
        print("[skip] 未找到 .venv/bin/pymarkdown，跳过通用 lint")
        return None
    cmd = [str(PYMARKDOWN), "-c", str(CONFIG), "scan", *[str(f) for f in files]]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    if output:
        print(output)
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Markdown 检查：加粗定界符 + 通用 lint")
    parser.add_argument("paths", nargs="*", default=[str(ROOT)], help="要扫描的文件或目录（默认本项目根）")
    parser.add_argument("--strict", action="store_true", help="通用 lint 问题也计入失败")
    args = parser.parse_args()

    files = list(iter_md_files(args.paths))
    if not files:
        print("未找到 .md 文件")
        return 0

    print(f"== MD-CJK-BOLD 加粗定界符检查（{len(files)} 个文件）==")
    flanking_issues = sum(scan_file(f) for f in files)
    if flanking_issues:
        print(f"→ 命中 {flanking_issues} 处")
    else:
        print("→ 通过")

    print("\n== pymarkdown 通用 lint ==")
    pm_rc = run_pymarkdown(files)

    if flanking_issues:
        return 1
    if args.strict and pm_rc:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
