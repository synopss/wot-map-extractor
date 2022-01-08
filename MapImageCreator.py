import os
import zipfile

from PIL import Image

import settings
from utils.string_utils import as_snake_case


class MapImageCreator:
    pack_dir = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages')

    STANDARD_CAP_SIZE = 100
    MAP_IMAGE_SIZE = 512

    map_info = {}
    map_code = None
    map_name = None

    upper_right: None
    bottom_left: None
    height: None
    width: None

    def __init__(self, map_code, map_name, map_info):
        upper_right = map_info['upper_right']
        bottom_left = map_info['bottom_left']
        self.map_info = map_info
        self.upper_right = upper_right
        self.bottom_left = bottom_left
        self.height = upper_right[1] - bottom_left[1]
        self.width = upper_right[0] - bottom_left[0]
        self.map_code = map_code
        self.map_name = map_name

    def create_map(self):
        self.__handle_standard_battle()

    def __handle_standard_battle(self):
        green_cap_coord = self.__get_cap_coordinates('green_cap')
        red_cap_coord = self.__get_cap_coordinates('red_cap')
        map_dir = os.path.join(self.pack_dir, self.map_code + '.pkg')
        if not os.path.exists(map_dir):
            return
        with zipfile.ZipFile(map_dir, 'r') as map_ref:
            image = self.__get_cap_image(map_ref)

            green_cap_image_size = self.__get_cap_image_size('green_cap_radius')
            green_cap_offset = round(green_cap_image_size / 2)

            red_cap_image_size = self.__get_cap_image_size('red_cap_radius')
            red_cap_offset = round(red_cap_image_size / 2)

            if green_cap_coord is not None:
                green_cap = Image.open('assets/green_cap.png', 'r')
                green_cap = green_cap.resize((green_cap_image_size, green_cap_image_size))
                green_cap_position = self.__get_item_position(green_cap_coord[0], green_cap_coord[1], green_cap_offset)
                image.paste(green_cap, green_cap_position, green_cap)

            if red_cap_coord is not None:
                red_cap = Image.open('assets/red_cap.png', 'r')
                red_cap = red_cap.resize((red_cap_image_size, red_cap_image_size))
                red_cap_position = self.__get_item_position(red_cap_coord[0], red_cap_coord[1], red_cap_offset)
                image.paste(red_cap, red_cap_position, red_cap)

            image.save(f'{settings.DEST_DIR}{as_snake_case(self.map_name)}.png')

    def __get_cap_image(self, map_ref):
        path = f'spaces/{self.map_code}/mmap.dds'
        img_bytes = map_ref.open(path)
        return Image.open(img_bytes)

    def __get_image_size(self, image):
        with image as img:
            width, height = img.size
        return width, height

    def __get_cap_image_size(self, team_cap_radius_index):
        if team_cap_radius_index in self.map_info is not None:
            return 2 * self.map_info[team_cap_radius_index] * self.MAP_IMAGE_SIZE / self.height
        return round(self.MAP_IMAGE_SIZE / self.height * self.STANDARD_CAP_SIZE)

    def __get_cap_coordinates(self, team_cap):
        if 'standard_battle' in self.map_info and team_cap in self.map_info['standard_battle']:
            return self.map_info['standard_battle'][team_cap]
        return None

    def __get_item_position(self, x, y, cap_offset):
        new_x = ((x - self.bottom_left[0]) / self.width) * self.MAP_IMAGE_SIZE - cap_offset
        new_y = (1 - ((y - self.bottom_left[1]) / self.height)) * self.MAP_IMAGE_SIZE - cap_offset
        return round(new_x), round(new_y)
