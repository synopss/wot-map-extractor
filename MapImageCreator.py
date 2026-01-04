import os
import zipfile

from PIL import Image

from settings import WOT_PATH_DEFAULT, STANDARD_BATTLE, ENCOUNTER_BATTLE, ASSAULT, ATT_DEF, GRAND_BATTLE, DEST_DIR, \
    ONSLAUGHT
from utils.string_utils import as_snake_case


class MapImageCreator:
    pack_dir = os.path.join(WOT_PATH_DEFAULT, 'res', 'packages')

    STANDARD_CAP_SIZE = 100
    STANDARD_SPAWN_SIZE = 50
    MAP_IMAGE_SIZE = 512

    map_info = {}
    map_code = None
    map_name = None

    __cap_image_size = None
    __spawn_image_size = None

    __spawn_offset = None
    __cap_offset = None

    argv = []

    def __init__(self, map_code, map_name, map_info, argv):
        self.map_info = map_info
        self.map_code = map_code
        self.map_name = map_name
        self.argv = argv
        self.set_bounding_box_by_game_mode()

    def height(self):
        return self.__upper_right[1] - self.__bottom_left[1]

    def width(self):
        return self.__upper_right[0] - self.__bottom_left[0]

    def set_bounding_box(self, upper_right, bottom_left):
        self.__upper_right = upper_right
        self.__bottom_left = bottom_left

    def set_bounding_box_by_game_mode(self, game_mode=None):
        if (game_mode == ONSLAUGHT and self.map_info.get('onslaught_upper_right')
                and self.map_info.get('onslaught_bottom_left')):
            self.set_bounding_box(self.map_info['onslaught_upper_right'], self.map_info['onslaught_bottom_left'])
        else:
            self.set_bounding_box(self.map_info['upper_right'], self.map_info['bottom_left'])
        self.__cap_image_size = self.__get_cap_image_size()
        self.__spawn_image_size = self.__get_spawn_image_size()
        self.__cap_offset = round(self.__cap_image_size / 2)
        self.__spawn_offset = round(self.__spawn_image_size / 2)

    def create_map(self):
        self.__handle_game_mode(STANDARD_BATTLE)
        self.__handle_game_mode(ENCOUNTER_BATTLE)
        self.__handle_game_mode(ASSAULT)
        self.__handle_game_mode(ATT_DEF)
        self.__handle_game_mode(GRAND_BATTLE)
        self.__handle_game_mode(ONSLAUGHT)
        if '-f' in self.argv:
            self.__handle_cover()

    def __handle_game_mode(self, game_mode):
        if game_mode in self.map_info and len(self.map_info[game_mode]) != 0:
            self.set_bounding_box_by_game_mode(game_mode)
            green_cap_coord = self.__get_cap_coordinates(game_mode, 'green_cap')
            red_cap_coord = self.__get_cap_coordinates(game_mode, 'red_cap')
            green_spawn_coord = self.__get_cap_coordinates(game_mode, 'green_spawn')
            red_spawn_coord = self.__get_cap_coordinates(game_mode, 'red_spawn')
            cap_point_coord = self.__get_cap_coordinates(game_mode, 'cap_point')
            airstrike_point_coord = self.__get_cap_coordinates(game_mode, 'airstrike')
            comms_point_coord = self.__get_cap_coordinates(game_mode, 'comms')
            map_dir = self.__get_map_dir()

            self.__create_image(map_dir, game_mode, green_cap_coord, red_cap_coord, green_spawn_coord, red_spawn_coord,
                                cap_point_coord, airstrike_point_coord, comms_point_coord)

    def __create_image(self, map_dir, game_mode, green_cap_coord, red_cap_coord, green_spawn_coord, red_spawn_coord,
                       cap_point_coord, airstrike_point_coord, comms_point_coord):
        if not os.path.exists(map_dir):
            return
        with zipfile.ZipFile(map_dir, 'r') as map_ref:
            self.map_image = self.__get_cap_image(map_ref, game_mode)

            self.__paste_point_on_map('green_cap', green_cap_coord, self.__cap_image_size, self.__cap_offset)
            self.__paste_point_on_map('red_cap', red_cap_coord, self.__cap_image_size, self.__cap_offset)
            self.__paste_point_on_map('green_spawn', green_spawn_coord, self.__spawn_image_size, self.__spawn_offset)
            self.__paste_point_on_map('red_spawn', red_spawn_coord, self.__spawn_image_size, self.__spawn_offset)
            self.__paste_point_on_map('encounter_cap', cap_point_coord, self.__cap_image_size, self.__cap_offset)
            self.__paste_point_on_map('airstrike', airstrike_point_coord, self.__spawn_image_size, self.__spawn_offset)
            self.__paste_point_on_map('comms', comms_point_coord, self.__spawn_image_size, self.__spawn_offset)

            self.map_image.save(self.__get_saving_path(game_mode), format='PNG', quality=95)

    def __paste_point_on_map(self, asset_name, coordinates, point_image_size, point_image_offset):
        if asset_name != 'encounter_cap':
            if coordinates is not None:
                for index, coord in enumerate(coordinates):
                    cap_number = ('' if index == 0 else '2') if asset_name == 'green_cap' else ''
                    point = Image.open(f'assets/{asset_name}{cap_number}.png', 'r')
                    point = point.resize((point_image_size, point_image_size), Image.LANCZOS)
                    point_position = self.__get_point_position(coord[0], coord[1], point_image_offset)
                    self.map_image.paste(point, point_position, point)
        else:
            if coordinates is not None:
                point = Image.open(f'assets/{asset_name}.png', 'r')
                point = point.resize((point_image_size, point_image_size), Image.LANCZOS)
                point_position = self.__get_point_position(coordinates[0], coordinates[1], point_image_offset)
                self.map_image.paste(point, point_position, point)

    def __handle_cover(self):
        map_dir = self.__get_map_dir()

        if not os.path.exists(map_dir):
            return
        with zipfile.ZipFile(map_dir, 'r') as map_ref:
            image = self.__get_cap_image(map_ref)
            image.save(self.__get_saving_path(), format='PNG', quality=95)

    def __get_saving_path(self, game_mode=None):
        if '-f' in self.argv:
            path = f'{DEST_DIR}{as_snake_case(self.map_name)}'
            if not os.path.exists(path):
                os.mkdir(path)
            if game_mode is None:
                return f'{path}\\cover.png'
            return f'{path}\\{game_mode}.png'
        return f'{DEST_DIR}\\{as_snake_case(self.map_name)}_{game_mode}.png'

    def __get_cap_image(self, map_ref, game_mode=''):
        if game_mode == ONSLAUGHT and f'spaces/{self.map_code}/mmap_comp7.dds' in map_ref.namelist():
            path = f'spaces/{self.map_code}/mmap_comp7.dds'
        else:
            path = f'spaces/{self.map_code}/mmap.dds'
        img_bytes = map_ref.open(path)
        return Image.open(img_bytes)

    def __get_cap_image_size(self):
        return round(self.MAP_IMAGE_SIZE / self.height() * self.STANDARD_CAP_SIZE)

    def __get_spawn_image_size(self):
        return round(self.MAP_IMAGE_SIZE / self.height() * self.STANDARD_SPAWN_SIZE)

    def __get_cap_coordinates(self, game_mode, team_cap):
        if game_mode in self.map_info and team_cap in self.map_info[game_mode]:
            return self.map_info[game_mode][team_cap]
        return None

    def __get_point_position(self, x, y, cap_offset):
        new_x = ((x - self.__bottom_left[0]) / self.width()) * self.MAP_IMAGE_SIZE - cap_offset
        new_y = (1 - ((y - self.__bottom_left[1]) / self.height())) * self.MAP_IMAGE_SIZE - cap_offset
        return round(new_x), round(new_y)

    def __get_map_dir(self):
        return os.path.join(self.pack_dir, self.map_code + '.pkg')
