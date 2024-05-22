from typing import List
from pyrogram.filters import create, Filter


def account_filter(id: int) -> Filter:
    return create(lambda _, app, __: app.me.id == id)

def text_filter(text: str|List[str]) -> Filter:
    return create(lambda _, __, msg: msg.text in (text if isinstance(text, list) else [text]))

def thread_filter(message_thread_id: int) -> Filter:
    return create(lambda _, __, msg: msg.message_thread_id==message_thread_id)

def flug_filter(flug: bool) -> Filter:
    return create(lambda *_: flug)