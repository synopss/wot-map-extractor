import os
import zipfile

import xml.etree.ElementTree as ET

import settings
from XmlUnpacker import XmlUnpacker


class MapInfoCreator:
    scripts_dir = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages', 'scripts.pkg')
    map_info = {}

    __xmlr = XmlUnpacker()

    def extract(self, map_name):
        with zipfile.ZipFile(self.scripts_dir, 'r') as pkg_ref:
            path = f'scripts/arena_defs/{map_name}.xml'
            with pkg_ref.open(path) as map_conf:
                nodes = self.__xmlr.read(map_conf)
                print(ET.tostring(nodes))
                self.__extract_map_size(nodes)
                self.__extract_standard_battle(nodes)
                self.__extract_encounter_battle(nodes)
            return self.map_info

    def __extract_map_size(self, nodes):
        self.map_info['upper_right'] = self.__get_upper_right(nodes)
        self.map_info['bottom_left'] = self.__get_bottom_left(nodes)

    def __extract_standard_battle(self, nodes):
        if 'standard_battle' in self.map_info:
            del self.map_info['standard_battle']
        if self.__get_standard_battle_node(nodes) is not None:
            self.map_info['standard_battle'] = {}
            self.__extract_standard_battle_green_cap(nodes)
            self.__extract_standard_battle_red_cap(nodes)
            self.__extract_standard_battle_green_spawn(nodes)
            self.__extract_standard_battle_red_spawn(nodes)

    def __extract_standard_battle_green_cap(self, nodes):
        green_cap = self.__get_green_point(nodes, 'ctf', 'cap_point')
        self.__set_game_mode_property('standard_battle', 'green_cap', green_cap)

    def __extract_standard_battle_red_cap(self, nodes):
        red_cap = self.__get_red_point(nodes, 'ctf', 'cap_point')
        self.__set_game_mode_property('standard_battle', 'red_cap', red_cap)

    def __get_standard_battle_node(self, nodes):
        return nodes.find('gameplayTypes').find('ctf')

    def __extract_encounter_battle(self, nodes):
        if 'encounter_battle' in self.map_info:
            del self.map_info['encounter_battle']
        if self.__get_encounter_battle_node(nodes) is not None:
            self.map_info['encounter_battle'] = {}
            self.__extract_encounter_battle_green_spawns(nodes)
            self.__extract_encounter_battle_red_spawns(nodes)
            self.__extract_encounter_cap_point(nodes)

    def __extract_standard_battle_green_spawn(self, nodes):
        green_spawn = self.__get_green_point(nodes, 'ctf', 'spawn')
        self.__set_game_mode_property('standard_battle', 'green_spawn', green_spawn)

    def __extract_standard_battle_red_spawn(self, nodes):
        red_spawn = self.__get_red_point(nodes, 'ctf', 'spawn')
        self.__set_game_mode_property('standard_battle', 'red_spawn', red_spawn)

    def __extract_encounter_battle_green_spawns(self, nodes):
        green_spawn = self.__get_green_point(nodes, 'domination', 'spawn')
        self.__set_game_mode_property('encounter_battle', 'green_spawn', green_spawn)

    def __extract_encounter_battle_red_spawns(self, nodes):
        red_spawn = self.__get_red_point(nodes, 'domination', 'spawn')
        self.__set_game_mode_property('encounter_battle', 'red_spawn', red_spawn)

    def __extract_encounter_cap_point(self, nodes):
        cap_point = self.__get_point(nodes, None, 'domination', 'cap_point')
        self.__set_game_mode_property('encounter_battle', 'cap_point', cap_point)

    def __get_encounter_battle_node(self, nodes):
        return nodes.find('gameplayTypes').find('domination')

    def __set_game_mode_property(self, game_mode, prop, coordinates):
        if coordinates is not None:
            self.map_info[game_mode][prop] = coordinates

    def __get_green_point(self, nodes, game_mode, point_type):
        return self.__get_point(nodes, 'team1', game_mode, point_type)

    def __get_red_point(self, nodes, game_mode, point_type):
        return self.__get_point(nodes, 'team2', game_mode, point_type)

    def __get_point(self, nodes, team, game_mode, point_type):
        # TODO: need some refactoring
        if game_mode == 'ctf':
            if point_type == 'cap_point':
                team_base_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamBasePositions')
            elif point_type == 'spawn':
                team_base_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamSpawnPoints')
            else:
                return None
        elif game_mode == 'domination':
            if point_type == 'spawn':
                team_base_position_node = nodes.find('gameplayTypes').find(game_mode).find('teamSpawnPoints')
            elif point_type == 'cap_point':
                return self.__as_parsed_coordinates(nodes.find('gameplayTypes').find(game_mode).find('controlPoint'))
            else:
                return None
        else:
            return None
        if team_base_position_node is not None:
            team_node = team_base_position_node.find(team)
            if team_node is not None:
                position_node = team_node.findall('position')
                if position_node:
                    data = []
                    for position in position_node:
                        data.append(self.__as_parsed_coordinates(position))
                    return data
                position1_node = team_node.findall('position1')
                if position1_node:
                    data = []
                    for position in position1_node:
                        data.append(self.__as_parsed_coordinates(position))
                    return data
                position2_node = team_node.findall('position2')
                if position2_node:
                    data = []
                    for position in position2_node:
                        data.append(self.__as_parsed_coordinates(position))
                    return data
        return None

    def __as_parsed_coordinates(self, node):
        string = node.text.strip(' ').split(' ')
        return [round(float(string[0])), round(float(string[1]))]

    def __get_upper_right(self, nodes):
        return self.__as_parsed_coordinates(nodes.find('boundingBox').find('upperRight'))

    def __get_bottom_left(self, nodes):
        return self.__as_parsed_coordinates(nodes.find('boundingBox').find('bottomLeft'))
