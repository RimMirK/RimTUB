from utils import (
    Cmd, helplist, get_group,
    Module, Command, Argument as Arg,
    escape, b, pre, code as code_html
)

from contextlib import redirect_stderr, redirect_stdout
import asyncio, time, aiohttp, sys
from traceback import print_exc
from io import StringIO

cmd = Cmd(get_group(__name__))

helplist.add_module(
    Module(
        "PythonRunner",
        description='Запускает код на Python',
        author="RimMirK",
        version='1.0.0'
    ).add_command(
        Command(['py'], [Arg('Код')], "Запустить код")
    ).add_command(
        Command(['rpy'], [Arg('Ответ на сообщение')], "Запускает код из отвеченного сообщения")
    )
)


async def aexec(code, *args, timeout=None):
    exec(
        f"async def __todo(client, message, *args):\n"
        + " app = client; "
        + " msg = m = message; "
        + " r = msg.reply_to_message; "
        + " u = msg.from_user; "
        + " p = print; "
        + " ru = getattr(r, 'from_user', None)\n"
        + "".join(f"\n {_l}" for _l in code.split("\n"))
    )

    f = StringIO()
    with redirect_stdout(f):
        await asyncio.wait_for(locals()["__todo"](*args), timeout=timeout)

    return f.getvalue()

def generate_random_string(length):
    import string, random
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))

async def paste_neko(code: str):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.post(
                "https://nekobin.com/api/documents",
                json={"content": code},
            ) as paste:
                paste.raise_for_status()
                result = await paste.json()
    except Exception:
        return "Pasting failed"
    else:
        return f"nekobin.com/{result['result']['key']}.py"

@cmd(["py", "rpy"])
async def python_exec(app, msg):
    if len(msg.command) == 1 and msg.command[0] != "rpy":
        return await msg.edit_text(b("Введи код!"))

    if msg.command[0] == "rpy":
        code = msg.reply_to_message.text or msg.reply_to_message.caption
    else:
        code = (msg.text or msg.caption).split(maxsplit=1)[1]

    await msg.edit_text(b("<emoji id=5821116867309210830>⏳</emoji> Выполняю...", False))

    try:
        start_time = time.perf_counter()
        result = await aexec(code, app, msg, timeout=5)
        stop_time = time.perf_counter()

        result = result.strip()

        if len(result) > 3072:
            result = await paste_neko(result)
        

        return await msg.edit_text(
            b("<emoji id=5418368536898713475>🐍</emoji> Python " + sys.version.split()[0], False) + "\n\n" +
            pre(code, 'python') + "\n\n" + (
                b("<emoji id=5472164874886846699>✨</emoji> Вывод:\n", False) + (
                    result if result.startswith('nekobin.com/')
                    else code_html(result)
                ) + '\n' if result.strip() != ''
                    else b("<emoji id=5465665476971471368>❌</emoji> Вывода нет\n", False)
            ) + "\n" +
            b(f"<emoji id=5298728804074666786>⏱</emoji> Выполнено за {round(stop_time - start_time, 5)}s.", False),

            disable_web_page_preview=True,
        )
    except TimeoutError:
        return await msg.edit_text(
            b("<emoji id=5418368536898713475>🐍</emoji> Python " + sys.version.split()[0], False) + "\n\n" +
            pre(code, 'python') + "\n\n" +
            b("<emoji id=5465665476971471368>❌</emoji> Время на исполнение кода исчерапно! TimeoutError"),

            disable_web_page_preview=True,
        )
    except Exception as e:
        err = StringIO()
        with redirect_stderr(err):
            print_exc()

        return await msg.edit_text(
            b("<emoji id=5418368536898713475>🐍</emoji> Python " + sys.version.split()[0], False) + "\n\n" +
            pre(code, 'python') + "\n\n" +
            f"<emoji id=5465665476971471368>❌</emoji> {b(e.__class__.__name__)}: {b(e)}\n"
                f"Traceback: {escape(await paste_neko(err.getvalue()))}",

            disable_web_page_preview=True,
        )


