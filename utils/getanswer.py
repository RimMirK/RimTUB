from convopyro import Conversation
from pyrogram import types, filters, enums
from pyrogram.filters import Filter
from .modify_pyrogram_client import ModifyPyrogramClient as Client
from typing import Any, Union, List
import asyncio

async def get_answer(
        client: Client,
        chat_id: int | str,
        main_filter: Filter = None,
        additional_filter: Filter = None,
        startswith: str | None = None,
        timeout: int = None,
        default: any = None
    ) -> types.Message | Any:
    Conversation(client)
    if main_filter is None: main_filter = filters.create(
        lambda _, __, upd:
            (upd.text or upd.caption or '').startswith(startswith or '')
            and upd.from_user
            and upd.chat.id == chat_id
    )
    if additional_filter:
        out_filter = main_filter & additional_filter
    else:
        out_filter = main_filter
    try:
        return await client.listen.Message(out_filter, timeout=timeout)
    except TimeoutError:
        return default
    


async def make_request(app,
    request: str, chat: Union[int, str], startswith: str = '',
    timeout: int = 60, default: any = None, typing: bool = True,
    additional_filter: Filter = None, **msg_kwargs
) -> types.Message:
    if typing:
        await app.send_chat_action(chat, enums.chat_action.ChatAction.TYPING)
        await asyncio.sleep(1)
    return await get_answer(
        app, 
        (await app.send_message(chat, request, **msg_kwargs)).chat.id,
        startswith=startswith,
        timeout=timeout,
        default=default,
        additional_filter=additional_filter
    )