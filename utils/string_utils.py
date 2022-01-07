from re import sub

from exceptions import StringUtilsError


def as_int(int_string):
    int_string = int_string.strip()
    if int_string.isdigit():
        return int(int_string)
    raise StringUtilsError(f'[as_int]: {int_string}')


def as_snake_case(string):
    return '_'.join(
        sub('([A-Z][a-z]+)', r' \1',
            sub('([A-Z]+)', r' \1',
                string.replace('-', ' '))).split()).lower()
