from utils import Cmd, get_group, helplist, Argument as Arg, Command, Module, b, i, code, ModifyPyrogramClient as Client
from pyrogram.types import Message

helplist.add_module(
    Module(
        "notes",
        description="заметки 2.0",
        author="@RimMirK",
        version='2.0.1'
    ).add_command(
        Command(
            ['addnote', 'setnote'], [Arg("название"), Arg("ответ")], 'создать заметку'
        )
    ).add_command(
        Command(
            'note', [Arg("название")], 'вывести заметку'
        )
    ).add_command(
        Command(
            ['notes', 'mynotes'], [], 'список заметок'
        )
    ).add_command(
        Command(
            ['delnote'], [Arg("название")], 'удалить заметку'
        )
    )
)

cmd = Cmd(get_group())

@cmd(["addnote", 'setnote'])
async def _naddnote(app: Client, msg: Message):
    r = msg.reply_to_message
    if not r:
        return await msg.edit(b("Ответь на сообщение!"))
    try:
        name = msg.text.split(maxsplit=1)[1]
    except:
        return await msg.edit(b("Напиши название заметки!"))
    saved_msg = await r.copy('me')
    warning_msg = await saved_msg.reply(b("Не удаляй это сообщение! Оно нужно для работы заметок!"), quote=True)
    await app.db.set('nnotes', name, saved_msg.id)
    await app.db.set('nnotes_meta', name, warning_msg.id)
    await msg.edit(b("Заметка ") + code(name) + b(" сохранена!"))

@cmd('note')
async def _nnote(app: Client, msg: Message):
    try:
        name = msg.text.split(maxsplit=1)[1]
    except:
        return await msg.edit(b("Напиши название заметки!"))
    
    note_msg_id = await app.db.get('nnotes', name)
    if note_msg_id is None:
        return await msg.edit(b("Заметка ") + code(name) + b(" не найдена!"))
    await app.copy_message(
        msg.chat.id, 'me', note_msg_id,
        reply_to_message_id=msg.reply_to_message_id,
        message_thread_id=msg.message_thread_id
    )
    await msg.delete()

@cmd(["notes", "mynotes"])
async def _mynotes(app: Client, msg):
    d = await app.db.getall('nnotes')

    if d:
        m = b('Твои заметки:\n')
        for name, note_msg_id in d.items():
            note_msg = await app.get_messages('me', note_msg_id)
            m += " - " + code(name) + " : "
            if note_msg.text:
                m += (
                    (note_msg.text[:15].replace("\n", ' ') + '...')
                    if len(note_msg.text) > 15
                    else note_msg.text.replace("\n", ' ')
                )
            elif note_msg.video:
                m += i('Видео')
            elif note_msg.photo:
                m += i("Фото")
            elif note_msg.sticker:
                m += i("Стикер")
            elif note_msg.animation:
                m += i("ГИФ")
            elif note_msg.document:
                m += i("Файл")
            elif note_msg.voice:
                m += i("ГС")
            elif note_msg.video_note:
                m += i("Кружочек")
            if note_msg.caption:
                m += " " + (
                    (note_msg.caption[:15].replace("\n", ' ') + '...')
                    if len(note_msg.caption) > 15
                    else note_msg.caption.replace("\n", ' ')
                )
            m += '\n'
            
            
        
    else:
        m = b('пусто!')
    await msg.edit(m)

@cmd("delnote")
async def _delnote(app: Client, msg):
    try:
        name = msg.text.split(maxsplit=1)[1]
    except:
        return await msg.edit(b("Напиши название заметки!"))

    note_msg_id = await app.db.get('nnotes', name)
    if note_msg_id is None:
        return await msg.edit(b("Заметка не найдена!"))
    
    await app.delete_messages('me', note_msg_id)
    await app.delete_messages('me', await app.db.get("nnotes_meta", name))
    
    await app.db.remove('nnotes', name)
    await app.db.remove('nnotes_meta', name)

    await msg.edit(b("Заметка ") + code(name) + b(" удалена!"))
