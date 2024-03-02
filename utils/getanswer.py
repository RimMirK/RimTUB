from convopyro import Conversation
from pyrogram import types, filters, enums
from .modify_pyrogram_client import ModifyPyrogramClient as Client
from typing import Union, List
import asyncio

async def get_answer(
        client: Client,
        message: types.Message,
        _filters: List[filter] = None,
        startswith: str | None = None,
        timeout: int = None,
        default: any = None
    ) -> types.Message:
    if _filters is None: _filters = []
    # answer: types.Message = await listen_message(client, message.chat.id, timeout)
    # return answer if answer else default
    Conversation(client)
    try: 
        return await client.listen.Message(
            filters.create(
                lambda _, __, upd=types.Message:
                    (upd.text or upd.caption or '').startswith(startswith or '')
                    and upd.from_user
                    and upd.chat.id == message.chat.id
            ), timeout=timeout)
    except TimeoutError:
        return default
    

async def get_answer_after_callback(
        client: Client,
        chat_id: Union[int, str],
        _filters: List[filter] = None,
        startswith: str | None = None,
        timeout: int = None,
        default: any = None
    ) -> types.Message:
    if _filters is None: _filters = []
    Conversation(client)
    # answer: types.Message = await listen_message(client, message.chat.id, timeout)
    # return answer if answer else default
    try: 
        return await client.listen.Message(
            filters.create(
                lambda _, __, upd=types.Message:
                    (upd.text or upd.caption).startswith(startswith)
                    and upd.from_user
                    and upd.chat.id == message.chat.id
            ), timeout=timeout)
    except TimeoutError:
        return default


async def make_request(app,
    request: str, chat: Union[int, str], startswith: str = '',
    timeout: int = 60, default: any = None, typing: bool = True
) -> types.Message:
    if typing:
        await app.send_chat_action(chat, enums.chat_action.ChatAction.TYPING)
        await asyncio.sleep(1)
    return await get_answer(
        app, 
        await app.send_message(chat, request),
        startswith=startswith,
        timeout=timeout,
        default=default
    )

async def make_request_callback(app, request: str, chat_id: Union[int, str], message_id: int, startswith: str = '', timeout: int = 60, default: any = None):
    await app.request_callback_answer(chat_id, message_id, request)
    return await get_answer_after_callback(
        app, 
        chat_id,
        startswith=startswith,
        timeout=timeout,
        default=default
    )
