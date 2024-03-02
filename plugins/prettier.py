from utils import (
    Cmd, helplist,
    Module, Command, Argument as Arg,
    pre, code, b,
    get_group, sec_to_str,
    pnum, pretty
)
import asyncio, json, ast
from pyrogram import errors, types
from pytimeparse.timeparse import timeparse

cmd = Cmd(get_group())


helplist.add_module(
    Module(
        'Prettier',
        author='@RimMirK',
        version='1.0.0',
        description="Делает из нечитаемого читаемое"
    ).add_command(
        Command(['pnum'], [Arg('число')], 'Вывести красиво число')
    ).add_command(
        Command(['ps2s', 'psec_to_str'], [Arg('секунды')], 'секунды в читаемое время')
    ).add_command(
        Command(['pt2s', 'ptext_to_str'], [Arg('время')], 'время в секунды')
    ).add_command(
        Command(['pjson'], [Arg('JSON')], 'в читаемый JSON')
    )
)

@cmd(['ps2s', 'psec_to_str'])
async def _s2s(_, msg):
    try:
        await msg.edit(b(sec_to_str(float(msg.text.split()[1]), False)))
    except:
        await msg.edit(b("Ошибка!"))

@cmd(['pnum'])
async def _pnum(_, msg):
    try:
        await msg.edit(b(f"{pnum(float(msg.text.split()[1])):,}"))
    except:
        await msg.edit(b("Ошибка!"))

@cmd(['pt2s', 'ptext_to_str'])
async def _pt2s(_, msg):
    try:
        await msg.edit(b(f"{timeparse(msg.text.split()[1])}"))
    except:
        await msg.edit(b("Ошибка!"))

@cmd('pjson')
async def _pjson(_, msg):
    try:
        await msg.edit(pre(f"{json.dumps(json.loads(msg.text.split(maxsplit=1)[1]), default=str, indent=4)}", 'JSON'))
    except Exception as e:
        print(e)
        await msg.edit(b("Ошибка!"))

@cmd('pdict')
async def _pdict(_, msg):
    try:
        await msg.edit(pre(f"{pretty(ast.literal_eval(msg.text.split(maxsplit=1)[1]), htchar=' ', indent=2)}", 'Python'))
    except Exception as e:
        raise e()
        await msg.edit(b("Ошибка!"))