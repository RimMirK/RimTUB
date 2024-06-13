from utils import Cmd, get_group, helplist, Argument as Arg, Command, Module, i, b, code, escape

helplist.add_module(
    Module(
        "formatter",
        description="Модуль который меняет формат сообщения",
        author="@RimMirK",
        version='1.0'
    ).add_command(
        Command(
            "i", [Arg("Текст")], 'сделать текст курсивом'
        )
    ).add_command(
        Command(
            'b', [Arg("Текст")], 'сделать текст жирным'
        )
    ).add_command(
         Command(
            'code', [Arg("Текст")], 'сделать текст моно'
        )
    ).add_command(
          Command(
            'inv', [Arg("Текст")], 'Сделать текст скрытым'
        )
   )
)


cmd = Cmd(get_group())

@cmd(['i'])
async def _i(_, msg):
    if len(msg.command) > 1:
        await msg.edit(i(msg.text.split(maxsplit=1)[1]))
        
@cmd(['b'])
async def _b(_, msg):
    if len(msg.command) > 1:
        await msg.edit(b(msg.text.split(maxsplit=1)[1]))
        
@cmd(['code'])
async def _code(_, msg):
    if len(msg.command) > 1:
        await msg.edit(code(msg.text.split(maxsplit=1)[1]))
        
@cmd(['inv'])
async def _inv(_, msg):
    if len(msg.command) > 1:
        await msg.edit("<spoiler>" + escape((msg.text.split(maxsplit=1)[1])) + "<spoiler>")