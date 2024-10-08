import os
import zipfile

from XmlUnpacker import XmlUnpacker
from settings import STANDARD_BATTLE, WOT_PATH_DEFAULT, STANDARD_BATTLE_CODE, ENCOUNTER_BATTLE_CODE, ENCOUNTER_BATTLE, \
    ASSAULT_CODE, ASSAULT, ATT_DEF, ATT_DEF_CODE, GRAND_BATTLE, GRAND_BATTLE_CODE, get_game_mode, ONSLAUGHT, \
    ONSLAUGHT_CODE, get_event_type


class MapInfoCreator:
    scripts_dir = os.path.join(WOT_PATH_DEFAULT, 'res', 'packages', 'scripts.pkg')
    map_info = {}
    __coordinates = []
    __team_spawn_position_node = None
    __event_position_node = None

    __xmlr = XmlUnpacker()

    def extract(self, map_name):
        with zipfile.ZipFile(self.scripts_dir, 'r') as pkg_ref:
            path = f'scripts/arena_defs/{map_name}.xml'
            with pkg_ref.open(path) as map_conf:
                nodes = self.__xmlr.read(map_conf)
                self.__extract_map_size(nodes)
                self.__extract_standard_battle(nodes)
                self.__extract_encounter_battle(nodes)
                self.__extract_assault(nodes)
                self.__extract_att_def(nodes)
                self.__extract_30v30(nodes)
                self.__extract_onslaught(nodes)
            return self.map_info

    def __extract_map_size(self, nodes, has_custom_onslaught_size=False):
        if has_custom_onslaught_size:
            self.map_info['onslaught_upper_right'] = self.get_upper_right(nodes)
            self.map_info['onslaught_bottom_left'] = self.get_bottom_left(nodes)
            return
        else:
            self.map_info.pop('onslaught_upper_right', None)
            self.map_info.pop('onslaught_bottom_left', None)
        self.map_info['upper_right'] = self.get_upper_right(nodes)
        self.map_info['bottom_left'] = self.get_bottom_left(nodes)

    def __extract_standard_battle(self, nodes):
        if STANDARD_BATTLE in self.map_info:
            del self.map_info[STANDARD_BATTLE]
        if nodes.find('gameplayTypes').find(STANDARD_BATTLE_CODE) is not None:
            self.map_info[STANDARD_BATTLE] = {}
            self.__extract_point(nodes, STANDARD_BATTLE_CODE, 'cap_point', 'green_cap')
            self.__extract_point(nodes, STANDARD_BATTLE_CODE, 'cap_point', 'red_cap')
            self.__extract_point(nodes, STANDARD_BATTLE_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, STANDARD_BATTLE_CODE, 'spawn', 'red_spawn')

    def __extract_encounter_battle(self, nodes):
        if ENCOUNTER_BATTLE in self.map_info:
            del self.map_info[ENCOUNTER_BATTLE]
        if nodes.find('gameplayTypes').find(ENCOUNTER_BATTLE_CODE) is not None:
            self.map_info[ENCOUNTER_BATTLE] = {}
            self.__extract_point(nodes, ENCOUNTER_BATTLE_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, ENCOUNTER_BATTLE_CODE, 'spawn', 'red_spawn')
            self.__extract_point(nodes, ENCOUNTER_BATTLE_CODE, 'cap_point', 'cap_point')

    def __extract_assault(self, nodes):
        if ASSAULT in self.map_info:
            del self.map_info[ASSAULT]
        if nodes.find('gameplayTypes').find(ASSAULT_CODE) is not None:
            self.map_info[ASSAULT] = {}
            self.__extract_point(nodes, ASSAULT_CODE, 'cap_point', 'green_cap')
            self.__extract_point(nodes, ASSAULT_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, ASSAULT_CODE, 'spawn', 'red_spawn')

    def __extract_att_def(self, nodes):
        if ATT_DEF in self.map_info:
            del self.map_info[ATT_DEF]
        if nodes.find('gameplayTypes').find(ATT_DEF_CODE) is not None:
            self.map_info[ATT_DEF] = {}
            self.__extract_point(nodes, ATT_DEF_CODE, 'cap_point', 'green_cap')
            self.__extract_point(nodes, ATT_DEF_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, ATT_DEF_CODE, 'spawn', 'red_spawn')

    def __extract_30v30(self, nodes):
        if GRAND_BATTLE in self.map_info:
            del self.map_info[GRAND_BATTLE]
        if nodes.find('gameplayTypes').find(GRAND_BATTLE_CODE) is not None:
            self.map_info[GRAND_BATTLE] = {}
            self.__extract_point(nodes, GRAND_BATTLE_CODE, 'cap_point', 'green_cap')
            self.__extract_point(nodes, GRAND_BATTLE_CODE, 'cap_point', 'red_cap')
            self.__extract_point(nodes, GRAND_BATTLE_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, GRAND_BATTLE_CODE, 'spawn', 'red_spawn')

    def __extract_onslaught(self, nodes):
        if ONSLAUGHT in self.map_info:
            del self.map_info[ONSLAUGHT]
        if nodes.find('gameplayTypes').find(ONSLAUGHT_CODE) is not None:
            self.map_info[ONSLAUGHT] = {}
            onslaught_nodes = nodes.find('gameplayTypes').find(ONSLAUGHT_CODE)
            has_custom_onslaught_size = onslaught_nodes.find('boundingBox')
            if has_custom_onslaught_size:
                self.__extract_map_size(onslaught_nodes, has_custom_onslaught_size)
            self.__extract_point(nodes, ONSLAUGHT_CODE, 'spawn', 'green_spawn')
            self.__extract_point(nodes, ONSLAUGHT_CODE, 'spawn', 'red_spawn')
            self.__extract_point(nodes, ONSLAUGHT_CODE, 'cap_point', 'cap_point')
            self.__extract_point(nodes, ONSLAUGHT_CODE, 'event', 'airstrike')
            self.__extract_point(nodes, ONSLAUGHT_CODE, 'event', 'comms')

    def __extract_point(self, nodes, game_mode, point_type, point_category):
        if point_category.startswith('green'):
            coordinates = self.__get_coordinates(nodes, 'team1', game_mode, point_type)
        elif point_category.startswith('red'):
            coordinates = self.__get_coordinates(nodes, 'team2', game_mode, point_type)
        elif point_category == 'cap_point':
            coordinates = self.__get_coordinates(nodes, None, game_mode, point_type)
        elif point_category == 'airstrike':
            coordinates = self.__get_coordinates(nodes, 'airstrike', game_mode, point_type)
        elif point_category == 'comms':
            coordinates = self.__get_coordinates(nodes, 'comms', game_mode, point_type)
        else:
            return
        self.__set_game_mode_property(get_game_mode(game_mode), point_category, coordinates)

    def __set_game_mode_property(self, game_mode, prop, coordinates):
        if coordinates is not None:
            self.map_info[game_mode][prop] = coordinates

    def __get_coordinates(self, nodes, team, game_mode, point_type):
        self.__team_spawn_position_node = None
        self.__set_game_mode_coordinates_node(game_mode, STANDARD_BATTLE_CODE, point_type, nodes)
        self.__set_game_mode_coordinates_node(game_mode, ASSAULT_CODE, point_type, nodes)
        self.__set_game_mode_coordinates_node(game_mode, ATT_DEF_CODE, point_type, nodes)
        self.__set_game_mode_coordinates_node(game_mode, GRAND_BATTLE_CODE, point_type, nodes)
        self.__set_game_mode_coordinates_node(game_mode, ONSLAUGHT_CODE, point_type, nodes)
        if game_mode == ENCOUNTER_BATTLE_CODE or game_mode == ONSLAUGHT_CODE:
            if point_type == 'spawn':
                self.__team_spawn_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamSpawnPoints')
            elif point_type == 'cap_point':
                return self.__as_parsed_coordinates(nodes.find('gameplayTypes').find(game_mode).find('controlPoint'))
            elif point_type == 'event':
                self.__event_position_node = nodes.find('gameplayTypes').find(game_mode).find('pointsOfInterestUDO')
            else:
                return None

        if self.__team_spawn_position_node is not None:
            team_node = self.__team_spawn_position_node.find(team)
            if team_node is not None:
                self.__coordinates = []
                self.__append_coordinates(team_node, 'position', game_mode)
                self.__append_coordinates(team_node, 'position1', game_mode)
                self.__append_coordinates(team_node, 'position2', game_mode)
                return self.__coordinates
        if self.__event_position_node is not None:
            event_node = self.__event_position_node.findall('point')
            if event_node is not None:
                self.__coordinates = []
                self.__append_coordinates(event_node, 'point', game_mode, team)
                return self.__coordinates
        return None

    def __set_game_mode_coordinates_node(self, game_mode, game_mode_code, point_type, nodes):
        if game_mode == game_mode_code:
            if point_type == 'cap_point':
                self.__team_spawn_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamBasePositions')
            elif point_type == 'spawn':
                self.__team_spawn_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamSpawnPoints')
            elif point_type == 'event':
                self.__event_position_node = nodes.find('gameplayTypes').find(game_mode).find('pointsOfInterestUDO')
            else:
                self.__team_spawn_position_node = None

    def __append_coordinates(self, node, point_name, game_mode, data=None):
        if game_mode == ONSLAUGHT_CODE and len(node) > 1:
            for node_item in node:
                if node_item.find('position') is not None and node_item.find('type').text == get_event_type(data):
                    self.__coordinates.append(self.__as_parsed_coordinates(node_item.find('position')))
            return self.__coordinates

        position_node = node.findall(point_name)
        if position_node:
            for position in position_node:
                self.__coordinates.append(self.__as_parsed_coordinates(position))
            return self.__coordinates

    def get_upper_right(self, nodes):
        return self.__as_parsed_coordinates(nodes.find('boundingBox').find('upperRight'))

    def get_bottom_left(self, nodes):
        return self.__as_parsed_coordinates(nodes.find('boundingBox').find('bottomLeft'))

    def __as_parsed_coordinates(self, node):
        string = node.text.strip(' ').split(' ')
        return [round(float(string[0])), round(float(string[1]))]
