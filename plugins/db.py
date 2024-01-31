from utils import Cmd, get_group, helplist, Argument as Arg, Command, Module, code


helplist.add_module(
    Module(
        "db",
        description="Управление БД",
        author="@RimMirK",
        version='1.0.0'
    ).add_command(
        Command(
            'sql', [Arg("sql")], 'Выполнить sql'
        )
    )
)

cmd = Cmd(get_group())


@cmd('sql')
async def _sql(app, msg):
    _, sql = msg.text.split(maxsplit=1)
    await msg.edit(code(str(await app.db.exec(sql)))) 