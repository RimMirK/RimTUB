import asyncio
from typing import Callable
from pyrogram import Client
from .database import Database, DictStorage, DatabaseFactory
from config.base_config import DATABASE_FILE, NAME
from datetime import datetime
from hashlib import sha256
from logging import Logger
from telebot.async_telebot import AsyncTeleBot

_on_ready_funcs: list = []

database = DatabaseFactory(DATABASE_FILE)

ev = asyncio.get_event_loop()
ev.run_until_complete(database.connect_db())

class ModifyPyrogramClient(Client):
    cl: Client
    db: Database
    st: DictStorage
    num: int
    logger: Logger
    info: Logger.info
    warning: Logger.warning
    error: Logger.error
    debug: Logger.debug
    critical: Logger.critical
    fatal: Logger.fatal
    log: Logger.log
    bot: AsyncTeleBot
    bot_username: str

    def __init__(self, *args, num: int, logger: Logger, bot: AsyncTeleBot, **kwargs):
        super().__init__(*args, **kwargs)

        self.st = DictStorage()
        self.num = num
        self.app_hash = sha256(bytes(str(self.phone_number).encode())).hexdigest()

        self.db = database.get_db(self.app_hash)
        
        self.logger   = logger
        self.info     = logger.info
        self.warning  = logger.warning
        self.error    = logger.error
        self.debug    = logger.debug
        self.critical = logger.critical
        self.fatal    = logger.fatal
        self.log      = logger.log
        
        self.bot = bot
    

    def start(self, *args, **kwargs):
        r = super().start(*args, **kwargs)
        
        self.bot_username = self.loop.run_until_complete(self.bot.get_me()).username
        
        for func in _on_ready_funcs:
            self.loop.create_task(func(self))

        return r

    def on_ready(self=None, *_, **__) -> Callable:
        def decorator(func: Callable):
            _on_ready_funcs.append(func)
        return decorator
