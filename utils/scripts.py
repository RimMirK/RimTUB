def get_script_directory():
    import os, sys
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)


from typing import Any

def get_args(text: str, default='') -> str|Any:
    try: return text.split(maxsplit=1)[1]
    except IndexError: return default


def sec_to_str(seconds: str) -> str:
    seconds = int(seconds)
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    o = ''
    if seconds:
        o += str(int(seconds)) + "c."
    if minutes:
        o = str(int(minutes)) + 'м.\xa0' + o
    if hours:
        o = str(int(hours)) + 'ч.\xa0' + o
    if days:
        o = str(int(days)) + 'д.\xa0' + o
    if o == '':
        o = '0'

    return o


def plural(num, words):
    num = int(list(str(num))[-1])
    match num:
        case 1:
            return words[0]
        case 2|3|4:
            return words[1]
        case _:
            return words[2]

import os, sys

def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)

def get_group(_name) -> int:
    return abs(hash(_name) // 15_000_000_000_000_000)