#!/usr/bin/env python3
import sys
from db_config import load_db_config_from_authserver

try:
    import pymysql
except ImportError:
    print("Missing dependency: pymysql")
    print("Install with: pip install pymysql")
    sys.exit(1)


debug = False


def main() -> None:
    mob_type = input("Select mob type (1 = neutral, 2 = aggressive): ").strip()
    if mob_type == "1":
        mob_filter = "(ct.flags_extra & 2) <> 0"
        mob_type_text = "neutral"
    elif mob_type == "2":
        mob_filter = "(ct.flags_extra & 2) = 0"
        mob_type_text = "aggressive"
    else:
        print("Invalid mob type. Expected 1 or 2.")
        return

    raw = input("Enter multiplier (float, example: 1.5 or -1.5): ").strip()
    try:
        factor = float(raw)
    except ValueError:
        print("Invalid multiplier. Expected float.")
        return

    if factor == 0:
        print("Multiplier cannot be 0.")
        return

    connection = pymysql.connect(
        **load_db_config_from_authserver(),
        cursorclass=pymysql.cursors.DictCursor,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW COLUMNS FROM creature LIKE 'id1'")
            has_id1 = cursor.fetchone() is not None
            creature_entry_column = "id1" if has_id1 else "id"

            cursor.execute(
                f"""
                SELECT COUNT(*) AS cnt
                FROM creature c
                JOIN creature_template ct ON ct.entry = c.{creature_entry_column}
                WHERE ct.rank <> 3
                  AND {mob_filter}
                """
            )
            row = cursor.fetchone()
            count = row["cnt"] if row else 0
            if count == 0:
                print(f"No target rows found (rank <> 3, mob type = {mob_type_text}).")
                connection.rollback()
                return

            if debug:
                cursor.execute(
                    f"""
                    SELECT ct.entry, ct.name, ct.flags_extra, ct.rank
                    FROM creature c
                    JOIN creature_template ct ON ct.entry = c.{creature_entry_column}
                    WHERE ct.rank <> 3
                      AND {mob_filter}
                    GROUP BY ct.entry, ct.name, ct.flags_extra, ct.rank
                    ORDER BY RAND()
                    LIMIT 50
                    """
                )
                rows = cursor.fetchall()
                print(f"DEBUG MODE: update skipped. Showing up to 50 rows for mob type = {mob_type_text}.")
                print("entry | name | flags_extra | rank")
                for row in rows:
                    print(f"{row['entry']} | {row['name']} | {row['flags_extra']} | {row['rank']}")
                connection.rollback()
                return

            if factor > 0:
                sql = f"""
                UPDATE creature c
                JOIN creature_template ct ON ct.entry = c.{creature_entry_column}
                SET c.spawntimesecs = GREATEST(1, CEIL(c.spawntimesecs * %s))
                WHERE ct.rank <> 3
                  AND {mob_filter}
                """
                cursor.execute(sql, (factor,))
                mode_text = f"multiplied by {factor}"
            else:
                scale = abs(factor)
                sql = f"""
                UPDATE creature c
                JOIN creature_template ct ON ct.entry = c.{creature_entry_column}
                SET c.spawntimesecs = GREATEST(1, CEIL(c.spawntimesecs / %s))
                WHERE ct.rank <> 3
                  AND {mob_filter}
                """
                cursor.execute(sql, (scale,))
                mode_text = f"divided by {scale} (because multiplier is negative)"

            affected = cursor.rowcount
            connection.commit()

            print(f"Done. Rows matched by filter: {count}")
            print(f"Rows updated: {affected}")
            print(f"Mob type filter: {mob_type_text}")
            print(f"Spawn time update mode: {mode_text}")
    except Exception as exc:
        connection.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
