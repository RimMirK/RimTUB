from pyrogram import __version__
from pyrogram.types import Message as M

from utils import (
    sec_to_str, plural, restart, get_args, get_group,
    Cmd, bot_uptime, helplist,
    b, a, code,
    HEADER,
    Module, Command, Argument as Arg,
)

from main import version
from config import PREFIX

import sys, time

cmd = Cmd(get_group())

@cmd(['me', 'start', 'menu'])
async def _me(_, msg: M):
    me_text = (
        HEADER + '\n'
        f"Версия: {b( version )}\n"
        f"Разработчик: {b(a('@RimMirK', 'https://t.me/RimMirK'), False)}\n"
        f"Канал: {b(a('@RimTUB', 'https://t.me/RimTUB'), False)}\n"
        f"Время работы: {b( sec_to_str(time.perf_counter() - bot_uptime))}\n"
        f"\n"
        f"<emoji id=5418368536898713475>🐍</emoji> Python: {b( sys.version.split()[0] )}\n"
        f"<emoji id=5246743576485832125>🔥</emoji> Pyrogram: {b( __version__ )}\n"
        f"ОС: {b( sys.platform )}\n"
        f"\n"
        f"Модули (плагины): {b(helplist.get_modules_count())}\n"
        f"Всего команд: {b(sum([*map(lambda i: i.get_commands_count(), helplist.get_modules())]))}\n"
        f"Всего возможностей: {b(sum([*map(lambda i: i.get_features_count(), helplist.get_modules())]))}"
    )
    await msg.edit(me_text)



@cmd(['help', 'h'])
async def _help(_, msg: M):
    if mod_name := get_args(msg.text or msg.caption).lower():
        mod = helplist.get_module(mod_name, lower=True)
        if not mod:
            return await msg.edit(f"Модуль {mod_name} не найден!\nПосмотреть список модулей: "+code(PREFIX+'help'))
        
        help_text = (
            HEADER + '\n\n' +
            f"Модуль {b(mod.name)}\n\n" +
            (f"Версия: {b(mod.version)}\n" if mod.version else '') +
            (f"Автор: {b(mod.author)}\n" if mod.author else '') +
            (f"Описание: {b(mod.description)}\n" if mod.description else '') +
            ("\n\n" if any((mod.version, mod.author, mod.description)) else '') +
            b(f"Команды ({mod.get_commands_count()}):") + "\n"
        )
        for c in mod.get_commands():
            help_text += (
                "  " + b(c.description) + "\n" +
                "  " + ("|".join((code(PREFIX+command) for command in c.commands))) + "  " + 
                (" ".join(list(map(str, c.args)))) + '\n\n'
            )

        help_text += b(f"\nВозможности ({mod.get_features_count()})")
        help_text += ":\n" if mod.get_features_count() > 0 else "\n"
        for f in mod.get_features():
            help_text += "  " + b(f.name) + ":\n"
            help_text += "    " + "\n    ".join(f.description.split('\n'))
            help_text += "\n\n"

        return await msg.edit(help_text)

    help_text = (
        HEADER + "\n"
        "\n"
        f"Модули (плагины): {b(helplist.get_modules_count())}\n"
    )
    commands_count = 0
    features_count = 0
    for module in helplist.get_modules():
        _commands_count = module.get_commands_count()
        _features_count = module.get_features_count()
        commands_count += _commands_count
        features_count += _features_count
        help_text += (
            f"    {code(module.name)} "
            f"({b(_commands_count)} {plural(_commands_count, ('команда', 'команды', 'команд'))} и "
            f"{ b(_features_count)} {plural(_features_count, ('возможность', 'возмоожности', 'возможностей'))})\n"
        )


    help_text += (
        f"(всего {b(commands_count)} {plural(commands_count, ('команда', 'команды', 'команд'))} и \n"
        f"{b(features_count)} {plural(features_count, ('возможность', 'возмоожности', 'возможностей'))})\n"
        f'\nДля получения списка команд модуля\nиспользуйте {code(PREFIX+"help")} [\xa0название\xa0модуля\xa0]'
    )

    await msg.edit(help_text)




@cmd(['restart', 'reload'])
async def _resatrt(app, msg):
    await msg.edit("Перезагружаюсь...")
    restart()



mod = Module(
    "Main",
    description="Главный модуль RimTUB. Помощь и управление тут",
    author="RimMirK",
    version='1.0.0'
)

mod.add_command(Command(['me', 'start', 'menu'], [Arg()], "Открыть стартовое меню"))
mod.add_command(Command(['help', 'h'], [Arg('название модуля', False)], "Получить помощь"))
mod.add_command(Command(['restart', 'reload'], [Arg()], "Перезапустить RimTUB"))

helplist.add_module(mod)
