from utils import ModifyPyrogramClient as Client
from telebot.types import InlineQuery, CallbackQuery as C
import gc

def find_function_by_id(func_id):
    for obj in gc.get_objects():
        if hasattr(obj, '__call__') and id(obj) == func_id:
            return obj
    return None


@Client.on_ready()
async def _on_ready(app: Client):
    @app.bot.inline_handler(lambda _: True)
    async def _all_inline(i: InlineQuery):
        user_id, func_id = map(int, i.query.split(':'))
        if i.from_user.id != user_id: return
        if func := find_function_by_id(func_id):
            await func(app, i)
    @app.bot.callback_query_handler(lambda _: True)
    async def _all_callback(c: C):
        user_id, func_id = map(int, c.data.split(':'))
        if c.from_user.id != user_id:
            return await app.bot.answer_callback_query(c.id, "❗️Это не твоя кнопка!", True)
        if func := find_function_by_id(func_id):
            await app.bot.answer_callback_query(c.id)
            return await func(app, c)
        await app.bot.answer_callback_query(c.id, "Произошла ошибка! Функция не надйена!", True)
            



