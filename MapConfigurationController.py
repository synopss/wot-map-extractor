import os
import zipfile

import settings
from XmlUnpacker import XmlUnpacker


class MapConfigurationController:
    scripts_dir = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages', 'scripts.pkg')
    map_info = {}

    xmlr = XmlUnpacker()

    def extract(self, map_name):
        with zipfile.ZipFile(self.scripts_dir, 'r') as pkg_ref:
            path = f'scripts/arena_defs/{map_name}.xml'
            with pkg_ref.open(path) as map_conf:
                nodes = self.xmlr.read(map_conf)
                self.__extract_map_size(nodes)
                self.__extract_standard_battle(nodes)
            return self.map_info

    def __extract_map_size(self, nodes):
        self.map_info['upper_right'] = self.__get_upper_right(nodes)
        self.map_info['bottom_left'] = self.__get_bottom_left(nodes)

    def __extract_standard_battle(self, nodes):
        if self.__get_standard_battle_node(nodes) is not None:
            self.map_info['standard_battle'] = {}
            green_cap = self.__get_green_cap(nodes)
            if green_cap is not None:
                self.map_info['standard_battle']['green_cap'] = green_cap
            red_cap = self.__get_red_cap(nodes)
            if red_cap is not None:
                self.map_info['standard_battle']['red_cap'] = red_cap

            green_cap_radius = self.__get_radius(nodes, 'team1')
            if green_cap_radius is not None:
                self.map_info['standard_battle']['green_cap_radius'] = green_cap_radius
            red_cap_radius = self.__get_radius(nodes, 'team2')
            if red_cap_radius is not None:
                self.map_info['standard_battle']['red_cap_radius'] = red_cap_radius

    def __get_standard_battle_node(self, nodes):
        return nodes.find('gameplayTypes').find('ctf')

    def __get_green_cap(self, nodes):
        return self.__get_cap(nodes, 'team1')

    def __get_red_cap(self, nodes):
        return self.__get_cap(nodes, 'team2')

    def __get_cap(self, nodes, team):
        team_base_position_node = self.__get_standard_battle_node(nodes).find('teamBasePositions')
        if team_base_position_node is not None:
            team_node = team_base_position_node.find(team)
            if team_node is not None:
                position_node = team_node.find('position')
                if position_node is not None:
                    return self.as_parsed_coordinates(position_node)
                position1_node = team_node.find('position1')
                if position1_node is not None:
                    return self.as_parsed_coordinates(position1_node)
                position2_node = team_node.find('position2')
                if position2_node is not None:
                    return self.as_parsed_coordinates(position2_node)
        return None

    def as_parsed_coordinates(self, node):
        string = node.text.strip(' ').split(' ')
        return [round(float(string[0])), round(float(string[1]))]

    def __get_radius(self, nodes, team):
        # Back in the days, cap circles could have different sizes, this get the radius property which is the radius of
        # the custom cap size, but it probably won't be used anymore.
        team_base_position_node = self.__get_standard_battle_node(nodes).find('teamBasePositions')
        if team_base_position_node is not None:
            team_node = team_base_position_node.find(team)
            if team_node is not None:
                radius_node = team_node.find('radius')
                if radius_node is not None:
                    return self.as_parsed_coordinates(radius_node)
                radius1_node = team_node.find('radius1')
                if radius1_node is not None:
                    return self.as_parsed_coordinates(radius1_node)
                radius2_node = team_node.find('radius2')
                if radius2_node is not None:
                    return self.as_parsed_coordinates(radius2_node)
        return None

    def __get_upper_right(self, nodes):
        return self.as_parsed_coordinates(nodes.find('boundingBox').find('upperRight'))

    def __get_bottom_left(self, nodes):
        return self.as_parsed_coordinates(nodes.find('boundingBox').find('bottomLeft'))
