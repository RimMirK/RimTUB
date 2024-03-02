from utils import Cmd, get_group, helplist, Argument as Arg, Command, Module, b, code



helplist.add_module(
    Module(
        "notes",
        description="заметки",
        author="@RimMirK",
        version='1.0.0'
    ).add_command(
        Command(
            ['addnote', 'setnote'], [Arg("название"), Arg("текст / ответ")], 'создать заметку'
        )
    ).add_command(
        Command(
            'note', [Arg("название")], 'вывести заметку'
        )
    ).add_command(
        Command(
            ['cnote', 'clearnote'], [Arg("название")], 'вывести только текст заметки'
        )
    ).add_command(
        Command(
            ['notes', 'mynotes'], [], 'список заметок'
        )
    ).add_command(
        Command(
            ['delnote', 'delnotes'], [Arg("название(-я)")], 'удалить заметку'
        )
    )
)

cmd = Cmd(get_group())


@cmd(['addnote', "setnote"])
async def _setnote(app, msg):
    _, *args = msg.text.split(maxsplit=2)

    if not args:
        return await msg.edit(b('неверный ввод данных!'))

    name = args[0]

    if len(args) > 1:
        text = args[1]
        text_html = msg.text.html.split(maxsplit=2)[-1]
    else:
        if r := msg.reply_to_message:
            text = msg.quote_text or r.text or r.caption
            text_html = text.html
        else:
            return await msg.edit(b('неверный ввод данных!'))
    
    await app.db.set("notes", name.lower(), {'html': text_html, 'text': text})
    
    await msg.edit(b(f"Заметка {code(name)} добавлена!", False))

@cmd(["note", "cnote", "clearnote"])
async def _note(app, msg):
    cmd, name = msg.text.split(maxsplit=1)
    
    note = await app.db.get('notes', name.lower())
    
    if note:
        if cmd[1] == 'c':
            return await msg.edit(note['html'])
        return await msg.edit(f"Заметка {b(name)}:\n\n{note['html']}")
    
    return await msg.edit(b(f"Заметка {code(name)} не найдена!", False))

@cmd(["notes", "mynotes"])
async def _mynotes(app, msg):
    d = await app.db.getall('notes')

    bn = '\n'

    if d:
        m = b('Твои заметки:\n')
        for key, note in d.items():
            m += f' - {code(key)} : {note["text"][:20].replace(bn, " ")}...\n'
    else:
        m = b('пусто!')
    await msg.edit(m)

@cmd(["delnote", "delnotes"])
async def _delnote(app, msg):
    _, *names = msg.text.split()

    if not names:
        return await msg.edit(b("Неверны ввод!"))

    for name in names:
        await app.db.remove('notes', name)

    await msg.edit(b("Готово!"))