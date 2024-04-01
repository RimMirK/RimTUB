from typing import Any
from .helplist import HelpList
from .modify_pyrogram_client import ModifyPyrogramClient as Client
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
            filters.command(commands, PREFIX) & filters.me
            & ~filters.forwarded,
            group=self.group
        )


import itertools
a = itertools.count()

def get_group() -> int:
    return next(a)

