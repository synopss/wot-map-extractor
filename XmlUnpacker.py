import base64
import xml.etree.ElementTree as ET
from struct import unpack

from exceptions import XmlUnpackerError


class XmlUnpacker:
    PACKED_HEADER = 0x62a14e45
    stream = None
    dict = []

    def read(self, stream):
        self.stream = stream
        if self.__is_packed():
            self.dict = self.__read_dictionary()
            root = ET.Element('root')
            self.__read_element(root)
            self.stream = None
            return root
        else:
            stream.seek(0)
            tree = ET.fromstring(stream.read().decode('UTF-8'))
            return tree

    def __read_element(self, _base):
        children_count = unpack('<H', self.stream.read(2))[0]
        descriptor = self.__read_data_descriptor()
        children = self.__read_element_descriptors(children_count)
        offset = self.__read_data(_base, 0, descriptor)
        for child in children:
            node = ET.SubElement(_base, self.dict[child['name_index']])
            offset = self.__read_data(node, offset, child['descriptor'])

    def __read_data_descriptor(self):
        data = self.stream.read(4)
        if data:
            end_type = unpack('<L', data)[0]
            return {'type': (end_type >> 28) + 0, 'end': end_type & 268435455, 'address': self.stream.tell()}
        else:
            raise XmlUnpackerError('Failed to read data descriptor')

    def __read_element_descriptors(self, count):
        descriptors = []
        for i in range(0, count):
            data = self.stream.read(2)
            if data:
                name_index = unpack('<H', data)[0]
                descriptor = self.__read_data_descriptor()
                descriptors.append({'descriptor': descriptor, 'name_index': name_index})
                continue
            else:
                raise XmlUnpackerError('Failed to read element descriptors')
        return descriptors

    def __read_data(self, element, offset, descriptor):
        length = descriptor['end'] - offset
        if descriptor['type'] == 0:
            self.__read_element(element)

        elif descriptor['type'] == 1:
            element.text = self.__read_string(length)

        elif descriptor['type'] == 2:
            element.text = str(self.__read_number(length))

        elif descriptor['type'] == 3:
            float_str = self.__read_float(length)
            str_data = float_str.split(' ')
            if len(str_data) == 12:
                for i in [0, 3, 6, 9]:
                    row = ET.SubElement(element, 'row{}'.format(i // 3))
                    row.text = '{} {} {}'.format(*str_data[i:i + 3])
            else:
                element.text = float_str

        elif descriptor['type'] == 4:
            element.text = 'true' if self.__read_boolean(length) else 'false'

        elif descriptor['type'] == 5:
            element.text = self.__read_base64(length)

        else:
            raise XmlUnpackerError('Unknown element type: %s' % descriptor['type'])

        return descriptor['end']

    def __read_string(self, length):
        if length:
            return self.stream.read(length).decode('UTF-8')
        return ''

    def __read_number(self, length):
        if length == 0:
            return 0
        else:
            data = self.stream.read(length)
            if length == 1:
                return unpack('b', data)[0]
            elif length == 2:
                return unpack('<H', data)[0]
            elif length == 4:
                return unpack('<L', data)[0]
            elif length == 8:
                return unpack('<Q', data)[0]
            else:
                raise XmlUnpackerError('Unknown number length')

    def __read_float(self, length):
        n = length // 4
        res = ''
        for i in range(0, n):
            if i != 0:
                res += ' '
            res += str(unpack('f', self.stream.read(4))[0])
        return res

    def __read_boolean(self, length):
        if length == 0:
            return False
        elif length == 1:
            b = unpack('B', self.stream.read(1))[0]
            if b == 1:
                return True
            return False
        else:
            raise XmlUnpackerError('Boolean with wrong length.')

    def __read_base64(self, length):
        return base64.b64encode(self.stream.read(length)).decode('UTF-8')

    def __read_dictionary(self):
        self.stream.seek(5)
        dictionary = []
        while True:
            entry = self.__read_asciiz()
            if not entry:
                break
            dictionary.append(entry)
        return dictionary

    def __read_asciiz(self):
        _str = ''
        while True:
            c = self.stream.read(1)
            if ord(c) == 0:
                break
            _str += c.decode('UTF-8', errors='ignore')
        return _str

    def __is_packed(self):
        self.stream.seek(0)
        header = unpack('I', self.stream.read(4))[0]
        if header != self.PACKED_HEADER:
            return False
        return True
