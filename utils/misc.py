from typing import Any
from .helplist import HelpList, singleton
from .database import Database
from .modify_pyrogram_client import ModifyPyrogramClient as Client
from config import DATABASE_FILE
from time import perf_counter

helplist = HelpList()

bot_uptime = perf_counter()


from pyrogram import filters
from config import PREFIX

class Cmd:
    group: int
    def __init__(self, group, /) -> None:
        self.group = group
    
    def __call__(self, commands: list) -> Any:
        return Client.on_message(
            filters.command(commands, PREFIX) & filters.me,
            group=self.group
        )


import itertools
a = itertools.count()

def get_group() -> int:
    return next(a)

