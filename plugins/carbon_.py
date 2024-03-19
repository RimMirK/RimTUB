
from utils import Cmd, get_group, helplist, Module, Command, Argument as Arg, get_args
from config.user_config import PREFIX, PHOTO_PARAMS
import time, os
from carbon import Carbon, CarbonOptions

cmd = Cmd(get_group())

cb = Carbon()

LOADING = '<emoji id=5821116867309210830>⏳</emoji> Загрузка...'

@cmd(['cb', 'carbon'])
async def _cb(_, msg):
    await msg.edit(LOADING)
    
    try: _, lang, code = msg.text.split(maxsplit=2)
    except ValueError:
        if r:=msg.reply_to_message:
            if lang := get_args(msg.text):
                code = msg.quote_text or r.text or r.caption
            else:
                return await msg.edit(f"Ипользуй <code>{PREFIX}{msg.command[0]}</code> < язык / auto > < код / ответ >")
        else:
            return await msg.edit(f"Ипользуй <code>{PREFIX}{msg.command[0]}</code> < язык / auto > < код / ответ >")
        
    
    image = await cb.generate(CarbonOptions(code=code, language=lang.capitalize(), **PHOTO_PARAMS))
    filename = f'temp/temp_{int(time.time())}.png'
    
    await image.save(filename)
    await (msg.reply_to_message or msg).reply_photo(filename, quote=True, quote_text=msg.quote_text)
    
    await msg.delete()
    os.remove(filename)
    

helplist.add_module(
    Module(
        'carbon',
        description="Работет на carbon.now.sh.\nМожно настроить в <code>config.user_config</code> -> <code>PHOTO_PARAMS</code>",
        author='@RimMirK',
        version='1.0.1',
    ).add_command(
        Command(['cb', 'carbon'], [Arg("язык / auto"), Arg("код / ответ")], 'Красивое фото из кода')
    )
)   
