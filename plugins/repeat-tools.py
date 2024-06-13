from utils import (
    Cmd, helplist,
    Module, Command, Argument as Arg,
    pre, code, b,
    get_group, sec_to_str,
)
import asyncio
from pyrogram import errors, types
from pytimeparse.timeparse import timeparse

cmd = Cmd(get_group())

helplist.add_module(
    Module(
        'RepeatTools',
        author='@RimMirK',
        version='1.0.3',
        description="Повторяет заданный текст определенное кол-во раз с определенной заддержкой."
    ).add_command(
        Command(['repeat', 'rep'],
                [Arg('сколько раз'), Arg('заддержка'), Arg('текст сообщения')],
                'Начать повторять сообщение', 
    )).add_command(
        Command(
            ["norepeat", 'stoprepeat', 'norep', 'stoprep'], [Arg('номер повторения')], 
            'Прекращает повторять сообщение'
    ))
)


@cmd(["repeat", 'rep'])
async def repeat(app, msg: types.Message):
    try:
        rep = app.st.get('rep', [])
        n = max(rep) + 1 if rep else 1
        rep.append(n)
        app.st.set('rep', rep)
        
        _, count, delay, *text = msg.text.split()
        text = ' '.join(text)
        delay = timeparse(delay)
        await msg.edit(
            f"Начинаю повторять сообщение {code(n)}"
            f"{pre(text)} {b(count)} раз с заддержкой в {b(sec_to_str(delay, False))}\n\n"
        )
        for _ in range(int(count)):
            if n not in app.st.get('rep', []): 
                await app.send_message(msg.chat.id, f"⛔ Перестал повторять сообщение {b(n)}")
                break
            await app.send_message(msg.chat.id, text, message_thread_id=msg.message_thread_id)
            
    except ValueError:
        from config import PREFIX
        await msg.edit(
            f"<emoji id=5300877490313509761>📛</emoji> Ошибка ввода данных!\n"
            f"Используй {code(PREFIX + msg.command[0])} {b('[сколько повторений] [с какой заддержкай] [текст]')} (без скобок)"
        )

@cmd(["norepeat", 'stoprepeat', 'norep', 'stoprep'])
async def norepeat(app, msg):
    try:
        _, n = msg.text.split()
        if n == '*':
            app.st.rep = []
        else:
            app.st.get('rep', []).remove(int(n))
        await msg.edit("оправил запрос на остановку. Остановится при отправке следующего сообщения (само сообщение уже не отправиться)")
    except:
        await msg.edit('<emoji id="5300877490313509761">📛</emoji> error')