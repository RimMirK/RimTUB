from pyrogram import __version__
from pyrogram.types import Message as M

from utils import (
    sec_to_str, plural, restart, get_args, get_group,
    Cmd, bot_uptime, helplist,
    b, a, code,
    HEADER,
    Module, Command, Argument as Arg,
    ModifyPyrogramClient as Client,
)

from main import version
from config import PREFIX, SHOW_HEADER_IN_HELP

import os, sys, time, time, json

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
        f"<emoji id=5215186239853964761>💿</emoji> ОС: {b( sys.platform )}\n"
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
            (HEADER + '\n\n' if SHOW_HEADER_IN_HELP else '') +
            f"Модуль {b(mod.name)}\n\n" +
            (f"Версия: {b(mod.version)}\n" if mod.version else '') +
            (f"Автор: {b(mod.author, False)}\n" if mod.author else '') +
            (f"Описание: {b(mod.description, False)}\n" if mod.description else '') +
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

        help_text += f"\n{b('Легенда: ')}\n   {code('< >')} – обязательный аргумент\n   {code('[ ]')} – необязательный аргумент.\n   {code(' / ')} – или"

        return await msg.edit(help_text)

    help_text = (
        (HEADER + "\n" if SHOW_HEADER_IN_HELP else '') + 
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
            f"    {code(module.name)}   " + (
                f"({b(_commands_count)} {plural(_commands_count, ('команда', 'команды', 'команд'))}"
                if _commands_count > 0 else ''
            ) + (' и ' if _commands_count > 0 and _features_count > 0 else '') + (
                f"{ b(_features_count)} {plural(_features_count, ('возможность', 'возмоожности', 'возможностей'))})\n"
                if _features_count > 0 else ')\n'
            )
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
    restart(app.app_hash, msg.chat.id, msg.id)

@Client.on_ready()
async def _on_start(app):
    if len(sys.argv) >= 2:
        _, type_, *values = sys.argv
        if type_ == 'restart':
            app_hash, time_, chat_id, msg_id = values
            if app.app_hash != app_hash:
                return
            now = time.perf_counter()
            delta = now - float(time_)
            await app.edit_message_text(int(chat_id), int(msg_id), f'Перезапущено за <b>{delta:.2f}s.</b>')



mod = Module(
    "Main",
    description="Главный модуль RimTUB. Помощь и управление тут",
    author="RimMirK",
    version='1.3.1'
)

mod.add_command(Command(['me', 'start', 'menu'], [], "Открыть стартовое меню"))
mod.add_command(Command(['help', 'h'], [Arg('название модуля', False)], "Получить помощь"))
mod.add_command(Command(['restart', 'reload'], [], "Перезапустить RimTUB"))

helplist.add_module(mod)
