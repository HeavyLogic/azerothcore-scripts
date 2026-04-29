#!/usr/bin/env python3
import sys
from db_config import load_db_config_from_authserver

try:
    import pymysql
except ImportError:
    print("Missing dependency: pymysql")
    print("Install with: pip install pymysql")
    sys.exit(1)


# ID рас в WoW 3.3.5a (Azerothcore)
races = {
    1: "Human",
    2: "Orc",
    3: "Dwarf",
    4: "Night Elf",
    5: "Undead",
    6: "Tauren",
    7: "Gnome",
    8: "Troll",
    10: "Blood Elf",
    11: "Draenei",
}

# ID классов
classes = {
    1: "Warrior",
    2: "Paladin",
    3: "Hunter",
    4: "Rogue",
    5: "Priest",
    6: "Death Knight",
    7: "Shaman",
    8: "Mage",
    9: "Warlock",
    11: "Druid",
}

# Словарь: класс ID -> список доступных рас ID
class_races = {
    1: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
    2: [1, 3, 7, 10, 11],
    3: [1, 3, 4, 7, 10, 2, 5, 6, 8],
    4: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
    5: [1, 3, 4, 7, 11, 2, 5, 6, 8, 10],
    6: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11],
    7: [11, 2, 6, 8, 10],
    8: [1, 3, 4, 7, 11, 2, 5, 6, 8, 10],
    9: [1, 3, 7, 11, 2, 5, 6, 8, 10],
    11: [4, 11, 10],
}


def main() -> None:
    nickname = input("Enter character nickname: ").strip()
    if not nickname:
        print("Nickname cannot be empty.")
        return

    print("Available classes:")
    for class_id, class_name in classes.items():
        print(f"{class_id} = {class_name}")
    class_raw = input("Enter class ID: ").strip()
    try:
        class_id = int(class_raw)
    except ValueError:
        print("Invalid class ID.")
        return

    if class_id not in classes:
        print("Unsupported class ID.")
        return

    available_races = class_races[class_id]
    print(f"Available races for {classes[class_id]}:")
    for race_id in available_races:
        print(f"{race_id} = {races[race_id]}")
    race_raw = input("Enter race ID: ").strip()
    try:
        race_id = int(race_raw)
    except ValueError:
        print("Invalid race ID.")
        return

    if race_id not in available_races:
        print(f"Race ID {race_id} is not available for class {classes[class_id]}.")
        return

    db_config = load_db_config_from_authserver()
    db_config["database"] = "acore_characters"
    connection = pymysql.connect(**db_config, cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT guid, name, race, class
                FROM characters
                WHERE name = %s
                LIMIT 1
                """,
                (nickname,),
            )
            row = cursor.fetchone()
            if row is None:
                print(f"Character '{nickname}' not found.")
                connection.rollback()
                return

            cursor.execute(
                """
                UPDATE characters
                SET race = %s, class = %s
                WHERE guid = %s
                """,
                (race_id, class_id, row["guid"]),
            )
            connection.commit()
            print(f"Done. Character: {row['name']}")
            print(f"Old race/class: {row['race']}/{row['class']}")
            print(f"New race/class: {race_id}/{class_id}")
            print(f"Race/class changed to {races[race_id]}/{classes[class_id]}.")
    except Exception as exc:
        connection.rollback()
        print(f"Error: {exc}")
        raise
    finally:
        connection.close()


if __name__ == "__main__":
    main()
