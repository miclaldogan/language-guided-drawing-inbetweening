#!/usr/bin/env bash
# Renders PlantUML sources to SVG + PNG (and PDF via rsvg-convert) using the pinned container image.
# Usage: tools/render.sh path/to/diagram.puml [...]
set -euo pipefail
IMAGE="plantuml/plantuml@sha256:9b5071ab56a4192aac458ab4b0d42261c22c8109695894ae5be6013c3be6cac1"  # PlantUML 1.2026.9, Graphviz 14.0.1
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for src in "$@"; do
  abs="$(realpath "$src")"; rel="${abs#"$ROOT"/}"
  for fmt in svg png; do
    docker run --rm -u "$(id -u):$(id -g)" -v "$ROOT":/work -w /work "$IMAGE" -charset UTF-8 -t$fmt "$rel"
  done
  base="${abs%.puml}"
  rsvg-convert -f pdf -o "$base.pdf" "$base.svg"
done
