if __name__ == '__main__':
    print("Запускаюсь...")


from pyrogram import idle
from pyrogram.enums.parse_mode import ParseMode

from config import API_ID, API_HASH, PHONES, PLAY_SOUND
from utils import get_script_directory, ModifyPyrogramClient

from sys import argv

play_sound = (True if len(argv) <= 1 else False) if PLAY_SOUND else False

if play_sound:
    from os import environ
    environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    from pygame.mixer import Sound, init

    init()

    s = Sound('started.mp3')

 
version = '1.3.1'


def start():
    for i, PHONE in enumerate(PHONES):
        cl = ModifyPyrogramClient(
            name="RimTUB" + (f'({i})' if i > 0 else ''),
            # skip_updates=False,
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
            num=i,
        )

        cl.start()

    if play_sound:
        s.play()


    print("\n- RimTUB Запущен и готов к работе! -\n")

    idle()

if __name__ == '__main__':
    start()