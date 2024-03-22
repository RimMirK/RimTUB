import asyncio
from typing import Callable
from pyrogram import Client
from .database import Database, DictStorage, DatabaseBase
from config.base_config import DATABASE_FILE, NAME
from datetime import datetime
from hashlib import sha256


_on_ready_funcs: list = []

database = DatabaseBase(DATABASE_FILE)

ev = asyncio.get_event_loop()
ev.run_until_complete(database.connect_db())

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

        self.db = database.get_db(self.app_hash)
    

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
        to_print = f'{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} '
        to_print += f'[{NAME}] '
        to_print += f'[{self.num}] ' if self else ''
        to_print += str(text)
        print(to_print, end=end)
