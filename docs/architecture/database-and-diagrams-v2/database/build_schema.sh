#!/usr/bin/env bash
# schema.sql = tüm *.up.sql dosyalarının sıralı birleşimi (tek doğruluk kaynağı: migrations/)
set -euo pipefail
cd "$(dirname "$0")"
{ echo "-- OTOMATİK ÜRETİLDİ: database/build_schema.sh. Elle düzenlemeyin; migrations/ kaynaktır."; cat migrations/*.up.sql; } > schema.sql
