from utils import (
    Cmd, helplist,
    Module, Command, Argument as Arg,
    pre, code, b,
    get_group
)
import asyncio
from pyrogram import errors, types

cmd = Cmd(get_group())

helplist.add_module(
    Module(
        'RepeatTools',
        author='@RimMirK',
        version='1.0.1',
        description="Повторяет заданный текст определенное кол-во раз с определенной заддержкой."
    ).add_command(
        Command(['repeat', 'rep'],
                [Arg('сколько раз'), Arg('с какой заддержкой (в секундах)'), Arg('текст сообщения')],
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
        app.st.rep = rep
        
        _, count, delay, *text = msg.command
        text = ' '.join(text)
        await msg.edit(
            f"Начинаю повторять сообщение {code(n)}"
            f"{pre(text)} {b(count)} раз с заддержкой в {b(delay)} сек.\n\n"
            f"Для исправления:{pre(msg.text, 'python')}"
        )
        for _ in range(int(count)):
            if n not in app.st.get('rep', []): 
                await app.send_message(msg.chat.id, f"⛔ Перестал повторять сообщение {b(n)}")
                break
            try: await app.send_message(msg.chat.id, text)
            except errors.flood_420.FloodWait as s:
                try: await asyncio.sleep(s)
                except: await asyncio.sleep(1)
                await app.send_message(msg.chat.id, text)
            await asyncio.sleep(float(delay))
    except ValueError:
        from config import PREFIX
        await msg.edit(
            f"<emoji id=5300877490313509761>📛</emoji> Ошибка ввода данных!\n"
            f"Используй {code(PREFIX + msg.command[0])} {b('[сколько повторений] [с какой заддержкай (в секундах)] [текст]')} (без скобок)"
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
