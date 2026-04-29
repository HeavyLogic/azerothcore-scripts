#!/usr/bin/env python3
import sys
from db_config import load_db_config_from_authserver

try:
    import pymysql
except ImportError:
    print("Missing dependency: pymysql")
    print("Install with: pip install pymysql")
    sys.exit(1)

def main() -> None:
    connection = pymysql.connect(
        **load_db_config_from_authserver(),
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT COUNT(*) AS cnt
                FROM creature_loot_template
                WHERE QuestRequired = 1
                """
            )
            row = cursor.fetchone()
            count = row["cnt"] if row else 0
            if count == 0:
                print("No rows found with QuestRequired = 1.")
                connection.rollback()
                return

            cursor.execute(
                """
                UPDATE creature_loot_template
                SET Chance = 100
                WHERE QuestRequired = 1
                """
            )
            affected = cursor.rowcount
            connection.commit()

            print(f"Done. Rows matched by filter: {count}")
            print(f"Rows updated: {affected}")
            print("Chance set to 100 for all QuestRequired = 1 rows.")
    except Exception as exc:
        connection.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
