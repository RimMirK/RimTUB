from utils import (
    Cmd, get_group, b, bq, code, helplist, Module, Command, Argument as Arg
)

from googletrans import Translator, LANGUAGES
translator = Translator()

cmd = Cmd(get_group())

LANGS = ''
for key, lang in LANGUAGES.items():
    LANGS += f"{code(key)}: {lang}\n"

@cmd(['tr', 'translate'])
async def _tr(_, msg):
    _, ln, *text = (msg.text or msg.caption).split(maxsplit=2)
    if text == []:
        if msg.reply_to_message:
            text = msg.quote_text or msg.reply_to_message.text
        else:
            return await msg.edit("Неверный ввод данных!")
    else:
        text = text[0]
    
    try:
        tr = translator.translate(text, ln)
        await msg.edit(
            f"{b(tr.src)}:\n{bq(text)}\n{b(tr.dest)}:\n{bq(tr.text)}"
        )
    except Exception as e:
        await msg.edit(f"{bq(text)}\n{b(f'{e.__class__.__name__}')}: {bq(str(e))}")
        
@cmd(['trf', 'translatefrom', 'trfrom'])
async def _trf(_, msg):
    _, src, ln, *text = (msg.text or msg.caption).split(maxsplit=3)
    if text == []:
        if msg.reply_to_message:
            text = msg.quote_text or msg.reply_to_message.text
        else:
            return await msg.edit("Неверный ввод данных!")
    else:
        text = text[0]
    
    try:
        tr = translator.translate(text, ln, src)
        await msg.edit(
            f"{b(tr.src)}:\n{bq(text)}\n{b(tr.dest)}:\n{bq(tr.text)}"
        )
    except Exception as e:
        await msg.edit(f"{bq(text)}\n{b(f'{e.__class__.__name__}')}: {bq(str(e))}")

@cmd('trlangs')
async def _trlangs(_, msg):
    await msg.edit(b("Доступные языки:\n")+LANGS) 
    

helplist.add_module(
    Module(
        "translate",
        description="Google переводчик",
        author="@RimMirK",
        version="1.1.2",
    ).add_command(
        Command(['tr', 'translate'], [Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trf', 'translatefrom', 'trfrom'], [Arg("Язык оригинала"), Arg("целевой язык"), Arg("текст/ответ")], "Перевести текст")
    ).add_command(
        Command(['trlangs'], [], "Список языков и их код")
    )
)
