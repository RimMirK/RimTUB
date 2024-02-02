def get_script_directory():
    import os, sys
    path = os.path.realpath(sys.argv[0])
    if os.path.isdir(path):
        return path
    else:
        return os.path.dirname(path)


from typing import Any, List

def get_args(text: str, default='') -> str|Any:
    try: return text.split(maxsplit=1)[1]
    except IndexError: return default

def pnum(num: int|float) -> int | float:
    return int(num) if int(num) == float(num) else float(num)

def sec_to_str(seconds: str, round: bool = True) -> str:
    seconds = int(seconds)
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
        o = '0'

    return o


def plural(num, words: List['str']):
    strnum = str(num)
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

import os, sys, json, time

def restart(app_id, chat_id=None, msg_id=None):
    # data = json.dumps(dict(
    #     type = "restart",
    #     time = time.perf_counter(),
    #     chat_id = chat_id,
    #     msg_id = msg_id,
    # ))
    # print(repr(data))
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
