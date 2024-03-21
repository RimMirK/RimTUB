def get_script_directory():
    import os, sys
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)


from typing import Any, List, Union

def get_args(text: str, default='') -> str|Any:
    try: return text.split(maxsplit=1)[1]
    except IndexError: return default

def pnum(num: int|float) -> int | float:
    return int(num) if int(num) == float(num) else float(num)

def sec_to_str(seconds: str, round: bool = True) -> str:
    seconds = float(seconds)
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    o = ''
    if seconds:
        o += str(int(seconds) if round else pnum(seconds)) + "c."
    if minutes:
        o = str(int(minutes)) + 'м.\xa0' + o
    if hours:
        o = str(int(hours)) + 'ч.\xa0' + o
    if days:
        o = str(int(days)) + 'д.\xa0' + o
    if o == '':
        o = '0c.'

    return o


def plural(num, words: List['str']):
    strnum = str(int(num))
    last_2_nums = int(''.join(strnum[-2:-1])) if len(strnum) >= 2 else None
    last_num = int(strnum[-1])

    if last_2_nums:
        if 11 <= last_2_nums <= 20:
            return words[2]
    
    match last_num:
        case 1:
            return words[0]
        case 2|3|4:
            return words[1]
        case _:
            return words[2]

import os, sys, time

def restart(app_id, chat_id=None, msg_id=None):
    os.execl(sys.executable, sys.executable, sys.argv[0],
        'restart', str(app_id),
        str(time.perf_counter()),
        str(chat_id), str(msg_id)
    )



def get_numbers_from_string(string) -> List[float]:
    import re
    nums = re.findall(r'\d*\.\d+|\d+', string)
    nums = [float(i) for i in nums]
    return nums


async def check_ping(app):
    import time

    a = time.perf_counter()
    m = await app.send_message('me', '.')
    b = time.perf_counter()
    await m.delete()
    c = time.perf_counter()

    delta = ((b - a) + (c - b)) / 2
    ping_ms = delta * 1000
    return ping_ms


from pyrogram.types import Message 

def get_args_raw(message: Union[Message, str], use_reply: bool = None) -> str:
    """
    https://github.com/KurimuzonAkuma/Kurimuzon-Userbot/blob/c43227443c13e4d959640f273724206dbbe4f9de/utils/scripts.py#L129

    Returns text after command.

    Args:
        message (Union[Message, str]): Message or text.

        use_reply (bool, optional): Try to get args from reply message if no args in message. Defaults to None.

    Returns:
        str: Text after command or empty string.
    """
    if isinstance(message, Message):
        text = message.text or message.caption
        args = text.split(maxsplit=1)[1] if len(text.split()) > 1 else ""

        if use_reply and not args:
            args = message.reply_to_message.text or message.reply_to_message.caption

    elif not isinstance(message, str):
        return ""

    return args or ""


def parse_amout(input_str, scheme: dict):
    import re

    match = re.search(r'(\d+(?:[,.]\d+)?)\s*([a-zA-Z]*)', input_str)
    
    if match:
        numeric_part = float(match.group(1).replace(',', '.'))
        unit = match.group(2)

        if unit:
            if unit in scheme:
                out = numeric_part * scheme[unit]
            else:
                raise ValueError()
        else:
            out = numeric_part
    else:
        raise ValueError()
    
    
    return out

def pretty(value, htchar='\t', lfchar='\n', indent=0, depth=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent*(depth+1), depth+1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + (htchar * (indent*(1)) if depth > 0 else ''))
    elif type(value) is list:
        items = [
            nlch + pretty(item, htchar, lfchar, indent*(depth+1), depth+1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + (htchar * (indent*(1)) if depth > 0 else ''))
    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent*(depth+1), depth+1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + (htchar * (indent*(1)) if depth > 0 else ''))
    else:
        return repr(value)
