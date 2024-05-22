import asyncio
import logging, coloredlogs
# logging.SPAM = 6
logger = logging.getLogger('RimTUB')
from config import LOGGING_LEVEL
logger.setLevel(LOGGING_LEVEL)
coloredlogs.install(logger=logger, level=logger.level,
    fmt='%(asctime)s %(name)s %(levelname)s: %(message)s'
)

# logging.log(logging.SPAM, 'sfdf')

if __name__ == '__main__':
    logger.info("Запускаюсь...")

from pyrogram import idle
from pyrogram.enums.parse_mode import ParseMode

from config import API_ID, API_HASH, PHONES, PLAY_SOUND
from utils import get_script_directory, ModifyPyrogramClient

from sys import argv

 
version = '1.6'

clients = []

def start():
    for i, PHONE in enumerate(PHONES):
        account_logger = logging.getLogger(f'RimTUB [{i}]')
        account_logger.setLevel(LOGGING_LEVEL)
        coloredlogs.install(logger=account_logger, level=logger.level,
            fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
            field_styles=dict(
                asctime=dict(color='green'),
                hostname=dict(color='magenta'),
                levelname=dict(color='black', bold=True),
                name=dict(color='blue'),
                programname=dict(color='cyan'),
                username=dict(color='yellow'),
                accid=dict(color='cyan')
            )
        )
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
            num=i,
            logger=account_logger
        )

        cl.start()
        clients.append(cl)

    if (True if len(argv) <= 1 else False) if PLAY_SOUND else False:
        
        from os import environ
        environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

        from pygame.mixer import Sound, init

        init()

        Sound('started.mp3').play()


    logger.info("\n\n- RimTUB Запущен и готов к работе! -\n")


    idle()
    for cl in clients:
        # cl: ModifyPyrogramClient
        cl.stop()


if __name__ == '__main__':
    start()