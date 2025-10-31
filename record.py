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
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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


ensure_table()
