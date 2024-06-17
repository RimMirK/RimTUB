from utils import helplist, Module, Command, Argument as Arg, Cmd, get_group, code, b
from pyrogram.types import Message
from config import PREFIX
import os

cmd = Cmd(get_group())


helplist.add_module(
    Module(
        "module_helper",
        description="Ваш помошник модулей",
        author="@RimMirK",
        version='1.1'
    ).add_command(
        Command(['dmf'], [Arg("ответ с файлом модуля")], "Скачать/обновить модуль")
    ).add_command(
        Command(['sm'], [Arg("Название модуля")], "Отправить модуль")
    ).add_command(
        Command(['delm'], [Arg("Название модуля")], "Удалить модуль")
    )
)


@cmd(['dmf'])
async def _dm(_, msg: Message):
    if r:= msg.reply_to_message:
        if r.document:
            if r.document.mime_type == 'text/x-python':
                pass
            else:
                return await msg.edit("<emoji id='5210952531676504517'>❌</emoji> Ошибка: Файл не является модулем!")
        else:
            return await msg.edit("<emoji id='5210952531676504517'>❌</emoji> Ошибка: Ответь на сообщение с модулем!")
    else:
        return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Ответь на сообщение!")

    await r.download(f'plugins//{r.document.file_name}')
    await msg.edit(
        "<emoji id='5206607081334906820'>✅</emoji> Модуль загружен!\n"
        f"\n<emoji id='5334544901428229844'>ℹ️</emoji> Перезагрузи RimTUB чтобы применить: {code(PREFIX + 'restart')}")

@cmd(['sm'])
async def _sm(_, msg: Message):
    try:
        _, name = msg.text.split(maxsplit=1)
    except ValueError:
        return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Напиши название модуля!")
    
    for row in os.walk("plugins/"):
        folder, _, files = row
        if folder == 'plugins/':
            for file in files:
                if file.lower() == name.lower() + ".py":
                    break
            else:
                return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")
    
    try:
        await msg.reply_document(f"plugins\\{file}")
        await msg.delete()
    except:
        await msg.edit("<emoji id='5260293700088511294'>⛔️</emoji> Произошла неизвестная ошибка!")
        
@cmd('delm')
async def _delm(app, msg):
    try:
        _, name = msg.text.split(maxsplit=1)
    except ValueError:
        return await msg.edit("<emoji id='5274099962655816924'>❗️</emoji> Напиши название модуля!")
    
    # file_path = 'путь/к/вашему/файлу.txt'

    for row in os.walk("plugins/"):
        folder, _, files = row
        if folder == 'plugins/':
            for file in files:
                if file.lower() == name.lower() + ".py":
                    break
            else:
                return await msg.edit("<emoji id='5447644880824181073'>⚠️</emoji> Такой модуль не найден!")


    os.remove(f'plugins\\{file}')
    await msg.edit(
        f"<emoji id='5445267414562389170'>🗑</emoji> Модуль {b(file.removesuffix('.py'))} удален!\n"
        f"\n<emoji id='5334544901428229844'>ℹ️</emoji> Перезагрузи RimTUB чтобы применить: {code(PREFIX + 'restart')}"
    )
