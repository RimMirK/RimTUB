from utils import (
    Cmd, helplist, pnum, b,
    Module, Command, Argument as Arg,
    get_group,
)
import python_weather
from translate import Translator
from pyrogram.types import Message as M

helplist.add_module(
    Module(
        "weather",
        description="Погода"
    ).add_command(
        Command("wt", [Arg('город')], 'показать погоду')
    )
)

cmd = Cmd(get_group())

tr = Translator(to_lang="ru")
wclient = python_weather.Client(locale=python_weather.Locale.RUSSIAN)

@cmd('wt')
async def _wt(_, msg: M):
    await msg.edit('<emoji id=5821116867309210830>⏳</emoji> Загрузка..')

    args = msg.text.split()
    if len(args) < 2:
        return await msg.reply("Введи город!")
    
    city = ' '.join(args[1:]).title()

    weather = await wclient.get(city)
    c = weather.current

    t  = f"📡 Сейчас в {b( city )} {b( tr.translate(c.description) )}, {b( c.temperature )}℃. Ощущается как {b (c.feels_like )}℃.\n"
    t += f"💧 Влажность: {b( c.humidity )}%\n"
    t += f"🌧 Осадки: {b( pnum(c.precipitation) )} мм\n"
    t += f"⏱ Давление: {b( pnum(c.pressure) )} psi\n"
    t += f"🌬 Ветер: {b( tr.translate(str(c.wind_direction)) )}, {b( c.wind_speed )} км/ч\n"
    t += f"☀️ Ультрафиолет: {b( tr.translate(str(c.ultraviolet)) )}"

    await msg.edit(t)