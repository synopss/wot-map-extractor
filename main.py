from MapImageCreator import MapImageCreator
from MapInfoCreator import MapInfoCreator
from utils.maps_utils import load_maps_dictionary


def main():
    for wot_map in load_maps_dictionary():
        map_code = wot_map[1]
        map_l10n_name = wot_map[2]
        print(map_l10n_name, map_code)
        map_info = MapInfoCreator().extract(map_code)
        print(map_info)
        MapImageCreator(map_code, map_l10n_name, map_info).create_map()


if __name__ == '__main__':
    main()
