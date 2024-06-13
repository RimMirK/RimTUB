from typing import overload, Awaitable
from utils import ModifyPyrogramClient
from pyrogram import Client

@overload
def format_callback(app: ModifyPyrogramClient | Client, func: Awaitable) -> str: ...
@overload
def format_callback(app: ModifyPyrogramClient | Client, func_id: int) -> str: ...
@overload
def format_callback(user_id: int, func: Awaitable) -> str: ...
@overload
def format_callback(user_id: int, func_id: int) -> str: ...

def format_callback(user: int | ModifyPyrogramClient | Client, func: int | Awaitable) -> str:
    return f"{user if isinstance(user, int) else user.me.id}:{func if isinstance(func, int) else id(func)}"