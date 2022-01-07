import gettext
import os
import zipfile

import settings
from XmlUnpacker import XmlUnpacker
from utils.string_utils import as_int


arenas_mo_gettext = None


def _a(str_):
    try:
        return arenas_mo_gettext.gettext(f'{str_}/name')
    except:
        return str_


def init():
    global arenas_mo_gettext

    arenas_mo_path = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'text', 'lc_messages', 'arenas.mo')
    if not os.path.exists(arenas_mo_path):
        raise FileNotFoundError(f"'{arenas_mo_path}' do not exists")

    arenas_mo_gettext = gettext.GNUTranslations(open(arenas_mo_path, 'rb'))


def load_maps_dictionary():
    init()
    package_file = 'scripts.pkg'
    package = os.path.join(settings.WOT_PATH_DEFAULT, 'res', 'packages', package_file)

    if package is None:
        raise FileNotFoundError(f"Failed to find package '{package_file}'")

    zfile = zipfile.ZipFile(package)
    file = '_list_.xml'
    file_path = find_file_handle(zfile, f'scripts/arena_defs/{file}')

    if file_path is None:
        raise FileNotFoundError(f"Failed to find open '{file}'")

    with zfile.open(file_path, 'r') as f:
        xmlr = XmlUnpacker()
        list_nodes = xmlr.read(f)

    maps_list = []
    for node in list_nodes.findall('map'):
        if node.find('id') is None or node.find('name') is None:
            return

        map_id = as_int(node.find('id').text)
        map_name = node.find('name').text.strip()
        map_l10n_name = _a(map_name)
        maps_list.append((map_id, map_name, map_l10n_name))

    return maps_list


def find_file_handle(zfile, package_file):
    for file in zfile.infolist():
        if file.filename.lower() == package_file.lower():
            return file
    return None
