from utils import (
    Cmd, helplist,
    Module, Command,
    i, b, get_group, make_request,
    ModifyPyrogramClient as Cl,
)

cmd = Cmd(get_group())

helplist.add_module(
    Module(
        "alerts",
        description="Для вывода актуальных данных про Воздушную Тревогу в Украине\n"
                    + i("(На основе @ air_alarm_ukraine_bot)") + "\n\n"
                    + b("Важно!") + "\n" + "С начала перейдите в бота и приймите соглашение"

    ).add_command(
        Command("almap", [], 'Показать карту')
    ).add_command(
        Command(['alreg', 'alactive'], [], 'Показать регионы с тревогой (текстом)')
    )
)


SAD = '<emoji id=5319007148565341481>☹️</emoji>'
LOADING = '<emoji id=5821116867309210830>⏳</emoji>'

CHAT = 'air_alarm_ukraine_bot'



@cmd(['almap'])
async def _almap(app, msg):
    await msg.edit(LOADING + " Загрузка")

    answer = await make_request(app, '/map', CHAT, timeout=10)

    if answer:
        await answer.copy(msg.chat.id)
        await msg.delete()
    else:
        await msg.edit(SAD + " Бот не ответил")


@cmd(['alreg', 'alactive'])
async def _alreg(app, msg):
    await msg.edit(LOADING + " Загрузка")

    answer = await make_request(app, '/active', CHAT, timeout=10)
    
    if answer:
        await msg.edit(answer.text.html)
    else:
        await msg.edit(SAD + " Бот не ответил")


