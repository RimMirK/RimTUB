from utils import Cmd, get_group, helplist, Module, Argument as Arg, Command
from pyrogram.types import Message as M, ChatPrivileges as CP
from pyrogram import Client as App

helplist.add_module(
    Module(
        "admin",
        description="Модуль для удобного администрирования чата",
        author="@RimMirK",
        version="1.0.0"
    ).add_command(
        Command('title', [Arg('Ответ на сообщение'), Arg('Ник')], "Установить ник (титулку)")
    )
)

cmd = Cmd(get_group())

@cmd(['title'])
async def _title(app: App, msg: M):
    if not msg.reply_to_message:
        return await msg.edit("Ответь на сообщение!")

    me = app.me
    try: me_member = await msg.chat.get_member(me.id)
    except: return await msg.edit("Тут нельзя устанавливать ники")

    user = msg.reply_to_message.from_user
    user_memeber = await msg.chat.get_member(user.id)


    if not me_member.privileges:
        return await msg.edit("Ты не админ")
    if not me_member.privileges.can_promote_members:
        return await msg.edit("Ты не можешь установливать ники")
    
    if user_memeber.promoted_by != app.me.id:
        await msg.chat.promote_member(user.id, CP())

    await app.set_administrator_title(
        msg.chat.id,
        user.id,
        msg.text.split(maxsplit=1)[1]
    )
    return await msg.edit("Готово")
    
    