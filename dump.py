import json

from record import create_conn, Entry


def dump():
    """Query all entries where marked == 1 and print them beautifully."""
    try:
        with create_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, message, marked FROM entries WHERE marked = %s", (1,))
                rows = cur.fetchall()

                entries = [Entry(**row) for row in rows]

                print("Marked Entries:")
                print(json.dumps([entry.__dict__ for entry in entries], ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Failed to fetch marked entries: {e}")


if __name__ == "__main__":
    dump()
