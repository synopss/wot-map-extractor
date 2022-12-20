# World of Tanks Map Extractor

This script is able to extract all maps with all game modes from the World of Tanks games files.

# Requirements

To work properly, this script needs you to install those libs:

- Pillow
- ElementTree

Made in Python 3.9

# Getting started

First thing to do : Go into settings.py and edit the ```WOT_PATH_DEFAULT``` and ```DEST_DIR``` constants to fit your needs.

By running
```
python main.py
```
You will have all map extracted to the folder you just defined.

### Arguments

```
python main.py -f
```
Will store all your images by maps, including a cover image (without cap points).

```
python main.py -f -j
```
Will create an extra json file with this format:

```json
{
    "name": "Ghost Town",
    "description": "Ghost Town",
    "cover": "./ghost_town/cover.png",
    "size": 1000,
    "views": [
        {
            "name": "Standard battle",
            "url": "./ghost_town/standard_battle.png"
        },
        {
            "name": "Encounter battle",
            "url": "./ghost_town/encounter_battle.png"
        },
        {
            "name": "Assault",
            "url": "./ghost_town/assault.png"
        },
        {
            "name": "Attack / Defense",
            "url": "./ghost_town/att_def.png"
        }
    ]
}
```

# Game mode available

- Standard Battle
- Encounter Battle
- Assault
- Attack / Defense
- Grand Battle
- Frontline
- Steel Hunter
- Onslaught
