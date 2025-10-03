~
#!/usr/bin/sh

set -e

SQLITE_DB_PATH="backend/db.sqlite3"

if [[ -fz "$SQLITE_DB_PATH" ]]; then
    cp "$SQLITE_DB_PATH" .

fi

python -m fastapi run