import asyncio
from typing import Callable
from pyrogram import Client
import pyrogram
from .database import Database, DictStorage
from .scripts import get_script_directory
from config.base_config import DATABASE_FILE
from inspect import currentframe, getframeinfo
from datetime import datetime
from pathlib import Path
from hashlib import sha256


_on_ready_funcs: list = []

class ModifyPyrogramClient(Client):
    cl: Client
    db: Database
    st: DictStorage
    num: int

    def __init__(self, *args, num: int, **kwargs):
        super().__init__(*args, **kwargs)

        self.st = DictStorage()
        self.num = num
        self.app_hash = sha256(bytes(str(self.phone_number).encode())).hexdigest()

        database = Database(self.app_hash)

        self.loop.run_until_complete(
            database.bootstrap(DATABASE_FILE)
        )
    
        self.db = database
    

    def start(self, *args, **kwargs):
        r = super().start(*args, **kwargs)
        
        for func in _on_ready_funcs:
            self.loop.create_task(func(self))

        return r

    def on_ready(self=None, *_, **__) -> Callable:
        def decorator(func: Callable):
            _on_ready_funcs.append(func)
        return decorator


    def print(self=None, text='', *, end='\n'):
        # frame = getframeinfo(currentframe().f_back)
        # path = Path(frame.filename)
        # rel = path.relative_to(
        #     self.workdir if self else
        #     Path(
        #         '\\'.join(
        #             Path(
        #                 get_script_directory()
        #             ).parents[-3:-1]
        #         )
        #     )
        # )

        to_print = ''
        to_print += datetime.now().strftime('%d-%m-%Y %H:%M:%S') + ' '
        to_print += '[RimTUB] '
        to_print += f'[{self.num}] ' if self else ''
        # to_print += ".".join([*rel.parts[:-1], rel.stem]) + "::"
        # to_print += str(frame.lineno) + ' | '
        to_print += text
        print(to_print, end=end)
