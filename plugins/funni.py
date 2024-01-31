from utils import Cmd, get_group, helplist, Argument as Arg, Command, Module
from config import TYPING_SYMBOL

from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified

import asyncio, random


helplist.add_module(
    Module(
        "funni",
        description="Плагин для веселья",
        author="@RimMirK",
        version='1.0.0'
    ).add_command(
        Command(
            'type', [Arg("Текст")], '"Напечатать" текст'
        )
    ).add_command(
        Command(
            'gpt_type', [Arg("Текст")], '"Напечатать" текст как будто его генерирует chatGPT'
        )
    )
)

cmd = Cmd(get_group())


@cmd('type')
async def _type(app, msg):
    _, text = msg.text.html.split(maxsplit=1)

    t = ''
    for l in text:  
        t += l
        await asyncio.sleep(random.uniform(0, 0.2))
        try: await msg.edit(t + TYPING_SYMBOL, parse_mode=ParseMode.DISABLED)
        except MessageNotModified:
            pass

    await asyncio.sleep(0.4)
    await msg.edit(t)


@cmd('gpt_type')
async def _gpt_type(app, msg):
    import random
    text = msg.text.html.split(maxsplit=1)[1]
    i = 0
    pieces= []
    while True:
        r = random.randint(3, 15)

        t = text[i:i+r]
        if t == '':
            break

        pieces.append(t)
        
        i += r

    t = ''

    for p in pieces:  
        t += p
        await asyncio.sleep(random.uniform(0, 0.5))
        try: await msg.edit(t + TYPING_SYMBOL, parse_mode=ParseMode.DISABLED)
        except MessageNotModified:
            pass

    await asyncio.sleep(0.4)
    await msg.edit(t)