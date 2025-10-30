from dataclasses import dataclass
import re
import json
import pymysql


@dataclass
class Entry:
    id: str
    message: str
    marked: int


db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'arboreal',
    'password': 'arborealpass',
    'database': 'arboreal',
}


def create_conn():
    conn = pymysql.connect(
        host=db_config.get('host', '127.0.0.1'),
        user=db_config.get('user', 'arboreal'),
        password=db_config.get('password', ''),
        database=db_config.get('database', 'arboreal'),
        port=int(db_config.get('port', 3306)),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
    return conn


def parse_entry(s: str, marked: int) -> Entry:
    if not isinstance(s, str):
        raise TypeError('input must be a string')

    m = re.search(r"#(\d+)", s)
    if not m:
        raise ValueError('no id found in string')
    _id = m.group(1)
    return Entry(id=_id, message=s.strip(), marked=marked)


def ensure_table():
    with create_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS entries
                (
                    id
                    VARCHAR
                (
                    64
                ) NOT NULL PRIMARY KEY,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    marked     int       default 0                 not null
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
            conn.commit()


def save_entry(entry: Entry):
    """Save an Entry into MySQL using pymysql.

    Performs an INSERT ... ON DUPLICATE KEY UPDATE to upsert the message.
    """
    if not isinstance(entry, Entry):
        raise TypeError('entry must be an Entry')

    try:
        with create_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO entries (id, message, marked)
                    VALUES (%s, %s, %s) ON DUPLICATE KEY
                    UPDATE message = VALUES(message), created_at = CURRENT_TIMESTAMP, marked = VALUES(marked)
                    """,
                    (entry.id, entry.message, entry.marked),
                )
                conn.commit()

    except Exception as e:
        print('ERROR' + e)


if __name__ == '__main__':
    # Demo multi-line input (same as provided by the user)
    demo = (
        "#7775002   2分钟前  10-30 19:04\n"
        "统计下不玩游戏的uu\n"
        "#35737087 刚刚 10-30 19:05\n"
        "[Alice] 1\n"
        "#35737091 刚刚 10-30 19:05\n"
        "[Bob] 不怎么玩\n"
    )

    entry = parse_entry(demo)
    # Basic sanity check / test
    assert entry.id == '7775002', f"unexpected id: {entry.id}"

    print('Parsed entry:')
    print(json.dumps({'id': entry.id, 'message': entry.message}, ensure_ascii=False, indent=2))

    # DB config matching docker-compose below; adjust as needed or use env vars

    # Try to save to DB; if DB isn't available the exception will surface.
    try:
        ensure_table()
        save_entry(entry)
        print('Saved entry to database (id=%s)' % entry.id)
    except Exception as e:
        print('Failed to save entry to database:', e)
