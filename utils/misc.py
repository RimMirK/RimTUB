from typing import Any
from .helplist import HelpList
from time import perf_counter

helplist = HelpList()

bot_uptime = perf_counter()


from pyrogram import Client, filters
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
