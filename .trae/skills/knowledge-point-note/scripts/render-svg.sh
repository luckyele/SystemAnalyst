#!/usr/bin/env bash
# 把 SVG 渲染成 PNG
# 用法: render-svg.sh <输入.svg> <输出.png> [缩放倍数，默认 2]
set -euo pipefail

svg=${1:?用法: render-svg.sh <输入.svg> <输出.png> [缩放倍数]}
png=${2:?用法: render-svg.sh <输入.svg> <输出.png> [缩放倍数]}
scale=${3:-2}

[ -f "$svg" ] || { echo "找不到 SVG: $svg" >&2; exit 1; }

w=$(grep -oP 'width="\K[0-9]+' "$svg" | head -1 || true)
h=$(grep -oP 'height="\K[0-9]+' "$svg" | head -1 || true)
[ -n "$w" ] && [ -n "$h" ] || { echo "SVG 根节点缺少 width/height 数字属性" >&2; exit 1; }

chrome=$(command -v google-chrome || command -v google-chrome-stable || command -v chromium || command -v chromium-browser || true)
[ -n "$chrome" ] || { echo "未找到 Chrome 或 Chromium" >&2; exit 1; }

"$chrome" --headless --disable-gpu --no-sandbox --hide-scrollbars \
  --force-device-scale-factor="$scale" \
  --window-size="$w,$h" \
  --default-background-color=ffffffff \
  --screenshot="$png" "$svg" >/dev/null 2>&1 || true

[ -s "$png" ] || { echo "渲染失败，未生成 $png" >&2; exit 1; }

size=$(identify -format '%wx%h' "$png" 2>/dev/null || echo "尺寸未知")
echo "已生成 $png ($size)"
