WOT_PATH_DEFAULT = 'C:\\Games\\World_of_Tanks'
DEST_DIR = 'C:\\Users\\Thomas\\Desktop\\test\\'

STANDARD_BATTLE_CODE = 'ctf'
ENCOUNTER_BATTLE_CODE = 'domination'
ASSAULT_CODE = 'assault'
ATT_DEF_CODE = 'assault2'

STANDARD_BATTLE = 'standard_battle'
ENCOUNTER_BATTLE = 'encounter_battle'
ASSAULT = 'assault'
ATT_DEF = 'att_def'


def get_game_mode(code):
    if code == STANDARD_BATTLE_CODE:
        return STANDARD_BATTLE
    if code == ENCOUNTER_BATTLE_CODE:
        return ENCOUNTER_BATTLE
    if code == ASSAULT_CODE:
        return ASSAULT
    if code == ATT_DEF_CODE:
        return ATT_DEF
