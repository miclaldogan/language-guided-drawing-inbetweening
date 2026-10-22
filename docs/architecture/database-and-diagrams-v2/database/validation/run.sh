#!/usr/bin/env bash
# Tek kullanımlık PostgreSQL 18 kapsayıcısında doğrulama paketini çalıştırır. Sistem Python'u değiştirilmez (uv, geçici ortam).
set -euo pipefail
cd "$(dirname "$0")"
uv run --python 3.11 --no-project --with 'psycopg[binary]==3.3.6' --with pytest==9.1.1 --with argon2-cffi==25.1.0 pytest -c pytest.ini "$@"
