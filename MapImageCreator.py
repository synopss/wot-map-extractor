import os
import zipfile

from PIL import Image

import settings
from utils.string_utils import as_snake_case


# TODO: need big refactoring after a lot of copypasta
class MapImageCreator:
    pack_dir = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages')

    STANDARD_CAP_SIZE = 100
    STANDARD_SPAWN_SIZE = 50
    MAP_IMAGE_SIZE = 512

    map_info = {}
    map_code = None
    map_name = None

    upper_right: None
    bottom_left: None
    height: None
    width: None

    argv = []

    def __init__(self, map_code, map_name, map_info, argv):
        upper_right = map_info['upper_right']
        bottom_left = map_info['bottom_left']
        self.map_info = map_info
        self.upper_right = upper_right
        self.bottom_left = bottom_left
        self.height = upper_right[1] - bottom_left[1]
        self.width = upper_right[0] - bottom_left[0]
        self.map_code = map_code
        self.map_name = map_name
        self.argv = argv

    def create_map(self):
        self.__handle_standard_battle()
        self.__handle_encounter_battle()
        self.__handle_assault()
        self.__handle_att_def()

    def __handle_standard_battle(self):
        if 'standard_battle' in self.map_info:
            green_cap_coord = self.__get_cap_coordinates('standard_battle', 'green_cap')
            red_cap_coord = self.__get_cap_coordinates('standard_battle', 'red_cap')
            green_spawn_coord = self.__get_cap_coordinates('standard_battle', 'green_spawn')
            red_spawn_coord = self.__get_cap_coordinates('standard_battle', 'red_spawn')
            map_dir = self.__get_map_dir()

            if not os.path.exists(map_dir):
                return
            with zipfile.ZipFile(map_dir, 'r') as map_ref:
                image = self.__get_cap_image(map_ref)

                green_cap_image_size = self.__get_cap_image_size()
                green_cap_offset = round(green_cap_image_size / 2)

                red_cap_image_size = self.__get_cap_image_size()
                red_cap_offset = round(red_cap_image_size / 2)

                if green_cap_coord is not None:
                    green_cap = Image.open('assets/green_cap.png', 'r')
                    green_cap = green_cap.resize((green_cap_image_size, green_cap_image_size))
                    green_cap_position = self.__get_item_position(green_cap_coord[0][0], green_cap_coord[0][1], green_cap_offset)
                    image.paste(green_cap, green_cap_position, green_cap)

                if red_cap_coord is not None:
                    red_cap = Image.open('assets/red_cap.png', 'r')
                    red_cap = red_cap.resize((red_cap_image_size, red_cap_image_size))
                    red_cap_position = self.__get_item_position(red_cap_coord[0][0], red_cap_coord[0][1], red_cap_offset)
                    image.paste(red_cap, red_cap_position, red_cap)

                green_spawn_image_size = self.__get_spawn_image_size()
                green_spawn_offset = round(green_spawn_image_size / 2)

                red_spawn_image_size = self.__get_spawn_image_size()
                red_spawn_offset = round(red_spawn_image_size / 2)

                if green_spawn_coord is not None:
                    for coord in green_spawn_coord:
                        green_cap = Image.open('assets/green_spawn.png', 'r')
                        green_cap = green_cap.resize((green_spawn_image_size, green_spawn_image_size))
                        green_cap_position = self.__get_item_position(coord[0], coord[1], green_spawn_offset)
                        image.paste(green_cap, green_cap_position, green_cap)

                if red_spawn_coord is not None:
                    for coord in red_spawn_coord:
                        red_cap = Image.open('assets/red_spawn.png', 'r')
                        red_cap = red_cap.resize((red_spawn_image_size, red_spawn_image_size))
                        red_cap_position = self.__get_item_position(coord[0], coord[1], red_spawn_offset)
                        image.paste(red_cap, red_cap_position, red_cap)

                image.save(f'{self.__get_saving_path()}{as_snake_case(self.map_name)}_standard_battle.png')

    def __handle_encounter_battle(self):
        if 'encounter_battle' in self.map_info:
            green_spawn_coord = self.__get_cap_coordinates('encounter_battle', 'green_spawn')
            red_spawn_coord = self.__get_cap_coordinates('encounter_battle', 'red_spawn')
            cap_point_coord = self.__get_cap_coordinates('encounter_battle', 'cap_point')
            map_dir = self.__get_map_dir()

            if not os.path.exists(map_dir):
                return
            with zipfile.ZipFile(map_dir, 'r') as map_ref:
                image = self.__get_cap_image(map_ref)

                green_spawn_image_size = self.__get_spawn_image_size()
                green_spawn_offset = round(green_spawn_image_size / 2)

                red_spawn_image_size = self.__get_spawn_image_size()
                red_spawn_offset = round(red_spawn_image_size / 2)

                if green_spawn_coord is not None:
                    for coord in green_spawn_coord:
                        green_cap = Image.open('assets/green_spawn.png', 'r')
                        green_cap = green_cap.resize((green_spawn_image_size, green_spawn_image_size))
                        green_cap_position = self.__get_item_position(coord[0], coord[1], green_spawn_offset)
                        image.paste(green_cap, green_cap_position, green_cap)

                if red_spawn_coord is not None:
                    for coord in red_spawn_coord:
                        red_cap = Image.open('assets/red_spawn.png', 'r')
                        red_cap = red_cap.resize((red_spawn_image_size, red_spawn_image_size))
                        red_cap_position = self.__get_item_position(coord[0], coord[1], red_spawn_offset)
                        image.paste(red_cap, red_cap_position, red_cap)

                cap_point_image_size = self.__get_cap_image_size()
                cap_point_offset = round(cap_point_image_size / 2)

                if cap_point_coord is not None:
                    cap_point = Image.open('assets/encounter_cap.png', 'r')
                    cap_point = cap_point.resize((cap_point_image_size, cap_point_image_size))
                    cap_point_position = self.__get_item_position(cap_point_coord[0], cap_point_coord[1], cap_point_offset)
                    image.paste(cap_point, cap_point_position, cap_point)

                image.save(f'{self.__get_saving_path()}{as_snake_case(self.map_name)}_encounter_battle.png')

    def __handle_assault(self):
        if 'assault' in self.map_info:
            green_cap_coord = self.__get_cap_coordinates('assault', 'green_cap')
            green_spawn_coord = self.__get_cap_coordinates('assault', 'green_spawn')
            red_spawn_coord = self.__get_cap_coordinates('assault', 'red_spawn')
            map_dir = self.__get_map_dir()

            if not os.path.exists(map_dir):
                return
            with zipfile.ZipFile(map_dir, 'r') as map_ref:
                image = self.__get_cap_image(map_ref)

                green_cap_image_size = self.__get_cap_image_size()
                green_cap_offset = round(green_cap_image_size / 2)

                if green_cap_coord is not None:
                    green_cap = Image.open('assets/green_cap.png', 'r')
                    green_cap = green_cap.resize((green_cap_image_size, green_cap_image_size))
                    green_cap_position = self.__get_item_position(green_cap_coord[0][0], green_cap_coord[0][1], green_cap_offset)
                    image.paste(green_cap, green_cap_position, green_cap)

                green_spawn_image_size = self.__get_spawn_image_size()
                green_spawn_offset = round(green_spawn_image_size / 2)

                red_spawn_image_size = self.__get_spawn_image_size()
                red_spawn_offset = round(red_spawn_image_size / 2)

                if green_spawn_coord is not None:
                    for coord in green_spawn_coord:
                        green_cap = Image.open('assets/green_spawn.png', 'r')
                        green_cap = green_cap.resize((green_spawn_image_size, green_spawn_image_size))
                        green_cap_position = self.__get_item_position(coord[0], coord[1], green_spawn_offset)
                        image.paste(green_cap, green_cap_position, green_cap)

                if red_spawn_coord is not None:
                    for coord in red_spawn_coord:
                        red_cap = Image.open('assets/red_spawn.png', 'r')
                        red_cap = red_cap.resize((red_spawn_image_size, red_spawn_image_size))
                        red_cap_position = self.__get_item_position(coord[0], coord[1], red_spawn_offset)
                        image.paste(red_cap, red_cap_position, red_cap)

                image.save(f'{self.__get_saving_path()}{as_snake_case(self.map_name)}_assault.png')

    def __handle_att_def(self):
        if 'att_def' in self.map_info:
            green_cap_coord = self.__get_cap_coordinates('att_def', 'green_cap')
            green_spawn_coord = self.__get_cap_coordinates('att_def', 'green_spawn')
            red_spawn_coord = self.__get_cap_coordinates('att_def', 'red_spawn')
            map_dir = self.__get_map_dir()

            if not os.path.exists(map_dir):
                return
            with zipfile.ZipFile(map_dir, 'r') as map_ref:
                image = self.__get_cap_image(map_ref)

                green_cap_image_size = self.__get_cap_image_size()
                green_cap_offset = round(green_cap_image_size / 2)

                if green_cap_coord is not None:
                    for index, coord in enumerate(green_cap_coord):
                        cap_number = '' if index == 0 else '2'
                        green_cap = Image.open(f'assets/green_cap{cap_number}.png', 'r')
                        green_cap = green_cap.resize((green_cap_image_size, green_cap_image_size))
                        green_cap_position = self.__get_item_position(coord[0], coord[1], green_cap_offset)
                        image.paste(green_cap, green_cap_position, green_cap)

                green_spawn_image_size = self.__get_spawn_image_size()
                green_spawn_offset = round(green_spawn_image_size / 2)

                red_spawn_image_size = self.__get_spawn_image_size()
                red_spawn_offset = round(red_spawn_image_size / 2)

                if green_spawn_coord is not None:
                    for coord in green_spawn_coord:
                        green_cap = Image.open('assets/green_spawn.png', 'r')
                        green_cap = green_cap.resize((green_spawn_image_size, green_spawn_image_size))
                        green_cap_position = self.__get_item_position(coord[0], coord[1], green_spawn_offset)
                        image.paste(green_cap, green_cap_position, green_cap)

                if red_spawn_coord is not None:
                    for coord in red_spawn_coord:
                        red_cap = Image.open('assets/red_spawn.png', 'r')
                        red_cap = red_cap.resize((red_spawn_image_size, red_spawn_image_size))
                        red_cap_position = self.__get_item_position(coord[0], coord[1], red_spawn_offset)
                        image.paste(red_cap, red_cap_position, red_cap)

                image.save(f'{self.__get_saving_path()}{as_snake_case(self.map_name)}_att_def.png')

    def __get_saving_path(self):
        if '-f' in self.argv:
            path = f'{settings.DEST_DIR}{as_snake_case(self.map_name)}'
            if not os.path.exists(path):
                os.mkdir(path)
            return f'{path}\\'
        return settings.DEST_DIR

    def __get_cap_image(self, map_ref):
        path = f'spaces/{self.map_code}/mmap.dds'
        img_bytes = map_ref.open(path)
        return Image.open(img_bytes)

    def __get_image_size(self, image):
        with image as img:
            width, height = img.size
        return width, height

    def __get_cap_image_size(self):
        return round(self.MAP_IMAGE_SIZE / self.height * self.STANDARD_CAP_SIZE)

    def __get_spawn_image_size(self):
        return round(self.MAP_IMAGE_SIZE / self.height * self.STANDARD_SPAWN_SIZE)

    def __get_cap_coordinates(self, game_mode, team_cap):
        if game_mode in self.map_info and team_cap in self.map_info[game_mode]:
            return self.map_info[game_mode][team_cap]
        return None

    def __get_item_position(self, x, y, cap_offset):
        new_x = ((x - self.bottom_left[0]) / self.width) * self.MAP_IMAGE_SIZE - cap_offset
        new_y = (1 - ((y - self.bottom_left[1]) / self.height)) * self.MAP_IMAGE_SIZE - cap_offset
        return round(new_x), round(new_y)

    def __get_map_dir(self):
        return os.path.join(self.pack_dir, self.map_code + '.pkg')
