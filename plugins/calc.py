from pyrogram import types
from utils import (
    code, Cmd, get_group, PREFIX,
    helplist, Module, Argument as Arg, Command
)


cmd = Cmd(get_group(__name__))

helplist.add_module(
    Module(
        "calc",
        version='1.1.0',
        author='@RimMirK',
        description="Калькулятор",
    ).add_command(
        Command(
            ['calc', 'eval'],
            [Arg("Выражение (пример)")],
            "Посчитать"
        )
    )
)

@cmd(['calc', 'eval'])
async def calc(_, msg: types.Message):
    _, equations = msg.text.split(maxsplit=1)
    
    i = (equations
        .replace('^','**')
        .replace('x', '*')
        .replace('х', '*')
        .replace('•', '*')
        .replace('·', '*')
        .replace('∙', '*')
        .replace(':', '/')
        .replace('÷', '/')
    )
    try:
        import math, utils
        
        def root(n: int|float, k: int|float = 2) -> float:
            return n ** (1/k)

        e = eval(i, globals(), locals())

        try: pe = int(e) if int(e) == e else e
        except: pe = e
        await msg.edit(f"<emoji id=5472164874886846699>✨</emoji> {equations} = {code(pe)}")
    except Exception as ex:
        print(ex)
        import traceback
        traceback.print_tb(ex.__traceback__)
        await msg.edit(f"<emoji id=5465665476971471368>❌</emoji> Error!\n\nДля исправления: {code(f'{PREFIX}{msg.command[0]} {equations}')}")