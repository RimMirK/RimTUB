if __name__ == '__main__':
    print("Запускаюсь...")


from pyrogram import idle
from pyrogram.enums.parse_mode import ParseMode

from config import API_ID, API_HASH, PHONES
from utils import get_script_directory, ModifyPyrogramClient


from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from pygame.mixer import Sound, init

init()

s = Sound('started.mp3')

 
version = '1.0.0'


def start():
    for i, PHONE in enumerate(PHONES):
        cl = ModifyPyrogramClient(
            name="RimTUB" + (f'({i})' if i > 0 else ''),
            api_id=API_ID,
            api_hash=API_HASH,
            phone_number=PHONE,
            app_version="1.0.0",
            lang_code="ru",
            plugins=dict(root='plugins'),
            workdir=get_script_directory(),
            hide_password=True,
            parse_mode=ParseMode.HTML,
            sleep_threshold=30,
            num=i
        )

        cl.start()


    s.play()
    print("RimTUB Запущен и готов к работе!")
    idle()

if __name__ == '__main__':
    start()