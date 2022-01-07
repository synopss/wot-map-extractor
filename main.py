import os
import zipfile

from PIL import Image

import settings
from MapConfigurationController import MapConfigurationController
from utils.maps_utils import load_maps_dictionary
from utils.string_utils import as_snake_case

pack_dir = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages')

standard_cap_size = 100
map_image_size = 512


def main():
    for wot_map in load_maps_dictionary():
        print(wot_map[2])
        map_info = MapConfigurationController().extract(wot_map[1])
        print(map_info)
        create_map(wot_map[1], wot_map[2], map_info)


def create_map(map_code, map_name, map_info):
    green_cap_coord = get_green_cap_coordinates(map_info)
    red_cap_coord = get_red_cap_coordinates(map_info)
    upper_right = map_info['upper_right']
    bottom_left = map_info['bottom_left']
    height = upper_right[1] - bottom_left[1]
    width = upper_right[0] - bottom_left[0]
    map_dir = os.path.join(pack_dir, map_code + '.pkg')
    if not os.path.exists(map_dir):
        return
    with zipfile.ZipFile(map_dir, 'r') as map_ref:
        path = f'spaces/{map_code}/mmap.dds'

        img_bytes = map_ref.open(path)
        image = Image.open(img_bytes)

        green_cap_image_size = get_cap_image_size(map_info, 'green_cap_radius', height)
        green_cap_offset = round(green_cap_image_size / 2)

        red_cap_image_size = get_cap_image_size(map_info, 'red_cap_radius', height)
        red_cap_offset = round(red_cap_image_size / 2)

        if green_cap_coord is not None:
            green_cap = Image.open('assets/green_cap.png', 'r')
            green_cap = green_cap.resize((green_cap_image_size, green_cap_image_size))
            green_cap_position = get_item_position(green_cap_coord[0], green_cap_coord[1], upper_right, bottom_left,
                                                   green_cap_offset)
            image.paste(green_cap, green_cap_position, green_cap)

        if red_cap_coord is not None:
            red_cap = Image.open('assets/red_cap.png', 'r')
            red_cap = red_cap.resize((red_cap_image_size, red_cap_image_size))
            red_cap_position = get_item_position(red_cap_coord[0], red_cap_coord[1], upper_right, bottom_left,
                                                 red_cap_offset)
            image.paste(red_cap, red_cap_position, red_cap)

        image.save(f'{settings.DEST_DIR}{as_snake_case(map_name)}.png')


def get_image_size(image):
    with image as img:
        width, height = img.size
    return width, height


def get_cap_image_size(map_info, team_cap_radius_index, height):
    if team_cap_radius_index in map_info is not None:
        return 2 * map_info[team_cap_radius_index] * map_image_size / height
    return round(map_image_size / height * standard_cap_size)


def get_green_cap_coordinates(map_info):
    if 'standard_battle' in map_info and 'green_cap' in map_info['standard_battle']:
        return map_info['standard_battle']['green_cap']
    return None


def get_red_cap_coordinates(map_info):
    if 'standard_battle' in map_info and 'red_cap' in map_info['standard_battle']:
        return map_info['standard_battle']['red_cap']
    return None


def get_item_position(x, y, upper_right, bottom_left, cap_offset):
    height = upper_right[1] - bottom_left[1]
    width = upper_right[0] - bottom_left[0]
    new_x = ((x - bottom_left[0]) / width) * map_image_size - cap_offset
    new_y = (1 - ((y - bottom_left[1]) / height)) * map_image_size - cap_offset
    return round(new_x), round(new_y)


if __name__ == '__main__':
    main()
