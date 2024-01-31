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


class ModifyPyrogramClient(Client):
    cl: Client
    db: Database
    st: DictStorage
    num: int

    def __init__(self, *args, num: int, **kwargs):
        self.num = num
        super().__init__(*args, **kwargs)

        self.st = DictStorage()

        database = Database(sha256(bytes(str(self.phone_number).encode())).hexdigest())

        self.loop.run_until_complete(
            database.bootstrap(DATABASE_FILE)
        )
    
        self.db = database
    
    def on_ready(self: Client = None, group: int = 0) -> Callable:
        def decorator(func: Callable):
            def wrapper(app: Client, *_):
                if app.st.get(f'get_raw{group}', True):
                    app.st.set(f'get_raw{group}', False)
                    print('return')
                    return asyncio.run(func(app))

            if isinstance(self, Client):
                self.add_handler(pyrogram.handlers.RawUpdateHandler(wrapper), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((pyrogram.handlers.RawUpdateHandler(wrapper), group))

            return func
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
