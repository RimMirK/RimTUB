from utils import (
    Cmd, get_group, b, bq, code, helplist, Module, Command, Argument as Arg
)
from bs4 import BeautifulSoup


cmd = Cmd(get_group())

@cmd(['emj', 'emjs'])
async def _emj(_, msg):
    html = getattr(msg.text, 'html', None) or getattr(msg.caption, 'html', None) or ''
    if r := msg.reply_to_message:
        html += getattr(msg.quote_text, 'html', None) or getattr(r.caption, 'html', None) or getattr(r.text, 'html', None) or ''
        
    bs = BeautifulSoup(html, 'lxml')
    emjs = bs.find_all('emoji')
    
    emojis = {}
    for emj in emjs:
        emojis[str(emj)] = (emj.attrs['id'])
    
    q1 = '"'
    q2 = "'"
    
    t = b('Custom Emojis:\n')
    for html, id_ in emojis.items():
        t += f"{html} : {code(id_)}\n{code(html)}\n{code(html.replace(q1, q2))}\n\n"
        
    await msg.edit(t)
    

helplist.add_module(
    Module(
        "emojis",
        description="Смотреть айди премиум емодзи",
        author='RimMirK',
        version='1.0.0'
    ).add_command(
        Command(['emj', 'emjs'], [Arg('текст с емодзи и/или ответ на сообщение с емодзи')], 'показать айди емодзи')
    )
)