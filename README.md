Some scripts I made for [Azerothcore WoTLK Repack](https://www.ownedcore.com/forums/world-of-warcraft/world-of-warcraft-emulator-servers/wow-emu-general-releases/1040387-azerothcore-wotlk-repack-playerbots-individual-progression-32-other-modules.html#post4501356).

## Contents

- **WoW Server.vbs** - for users of [Windows Terminal](https://apps.microsoft.com/detail/9n0dx20hk701). It opens DB, auth server, and world server in one Windows Terminal window with 3 tabs. Then it launches the client if `Wow.lnk` exists in your server folder.
- **db_config.py** - shared DB config loader for Python scripts. It reads connection settings from `configs/authserver.conf`.
- **update_creature_respawn.py** - changes respawn time for all non-boss mobs. You can set different multipliers for aggressive and neutral mobs.
- **update_quest_loot_chance.py** - sets drop chance to 100% for all quest-required creature loot (`QuestRequired = 1`).
- **update_character_race_class.py** - updates a character's race and class in `acore_characters`. It asks for character name and class first, then shows only races supported by that class.

## Requirements

- Python 3.x
- `pymysql` Python package (install with `py -m pip install pymysql`)
- Windows Terminal (optional, only needed for `WoW Server.vbs`)

## Installation

1. Download or copy these files into your Azerothcore server folder (the same folder where `worldserver.exe` is located).

## How to Run Python Scripts

1. Open Command Prompt (`cmd`).
2. Go to your server folder: `cd "D:\Games\Azerothcore WoTLK Repack"`
3. Run a script: `py update_creature_respawn.py`