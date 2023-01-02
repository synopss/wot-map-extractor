import json
import sys

from MapImageCreator import MapImageCreator
from MapInfoCreator import MapInfoCreator
from settings import DEST_DIR, STANDARD_BATTLE, ENCOUNTER_BATTLE, ASSAULT, ATT_DEF, GRAND_BATTLE, ONSLAUGHT
from utils.maps_utils import load_maps_dictionary
from utils.string_utils import as_snake_case


def main(argv):
    json_string = []
    for wot_map in load_maps_dictionary():
        map_code = wot_map[1]
        map_l10n_name = wot_map[2]
        map_info = MapInfoCreator().extract(map_code)
        MapImageCreator(map_code, map_l10n_name, map_info, argv).create_map()
        json_string.append(get_json(map_l10n_name, map_info, map_code))

    if '-j' in argv and '-f' in argv:
        with open(f'{DEST_DIR}\\output.json', 'w') as outfile:
            json.dump(json_string, outfile, indent=4)


def get_json(map_name, map_info, map_code):
    data = {'name': map_name, 'description': map_name, 'code': map_code, 'cover': f'./{as_snake_case(map_name)}/cover.png',
            'size': map_info['upper_right'][0] - map_info['bottom_left'][0], 'views': []}
    if STANDARD_BATTLE in map_info:
        if len(map_info[STANDARD_BATTLE]) == 0:
            data['views'].append({'name': 'Steel Hunter', 'url': f'./{as_snake_case(map_name)}/cover.png'})
        else:
            data['views'].append({'name': 'Standard battle', 'url': f'./{as_snake_case(map_name)}/{STANDARD_BATTLE}.png'})
    if ENCOUNTER_BATTLE in map_info:
        data['views'].append({'name': 'Encounter battle', 'url': f'./{as_snake_case(map_name)}/{ENCOUNTER_BATTLE}.png'})
    if ASSAULT in map_info:
        data['views'].append({'name': 'Assault', 'url': f'./{as_snake_case(map_name)}/{ASSAULT}.png'})
    if ATT_DEF in map_info:
        data['views'].append({'name': 'Attack / Defense', 'url': f'./{as_snake_case(map_name)}/{ATT_DEF}.png'})
    if GRAND_BATTLE in map_info:
        data['views'].append({'name': 'Grand Battle', 'url': f'./{as_snake_case(map_name)}/{GRAND_BATTLE}.png'})
    if ONSLAUGHT in map_info:
        data['views'].append({'name': 'Onslaught', 'url': f'./{as_snake_case(map_name)}/{ONSLAUGHT}.png'})
    if not data['views']:
        data['views'].append({'name': 'Frontline', 'url': f'./{as_snake_case(map_name)}/cover.png'})
    return data


if __name__ == '__main__':
    main(sys.argv[1:])
