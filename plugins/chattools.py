from pyrogram import Client, types, enums
from config import DELETED_MESSAGES_CHAT_ID, DELETED_MESSAGES_FILTERS
from utils import code, a, b, Cmd, get_group, helplist, Module, Command, Feature, PREFIX, check_ping
import asyncio

helplist.add_module(
    Module(
        "ChatTools",
        description="Инструменты для работы с чатами",
        version="1.2.0",
        author="@RimMirK"
    ).add_command(
        Command(['id', 'chatid', 'cid'], [], "Показать ID чата")
    ).add_command(
        Command(['chat', 'c'], [], "Получить всю информацию о чате")
    ).add_feature(
        Feature(
            "Нет удаленным сообщений", 
            f"Сохраняет удаленные сообщения.\n"
            f"Для работы требуется указать {b('config.user_config.DELETED_MESSAGES_CHAT_ID')}."
        )
    ).add_command(
        Command(['online'], [], "Сделать себя всегда онлайн")
    ).add_command(
        Command(['offline'], [], "Отменить всегда онлайн")
    ).add_command(
        Command(['ping'], [], "Узнать пинг")
    )
)

G = get_group()
cmd = Cmd(G)

@cmd(['id', 'chatid', 'cid'])
async def _id(_, msg):
    await msg.edit("ID Чата: " + code(msg.chat.id))

@cmd(['chat', 'c'])
async def _chat(_, msg):
    await msg.edit("Объект чата: " + code(msg.chat))

@cmd(['ping'])
async def _ping(app, msg):
    ping = await check_ping(app)

    if ping <= 100:
        e = '<emoji id="5294160616729096737">🟢</emoji>'
    elif ping <= 200:
        e = '<emoji id="5294234838058938175">🟡</emoji>'
    else:
        e = '<emoji id="5291899179008798421">🔴</emoji>'
        
    await msg.edit(b(f"Pong!{e}\nPing: {ping:.1f}ms", False))


messages: dict[int, dict[int, types.Message]] = {}


if DELETED_MESSAGES_CHAT_ID:
    @Client.on_message(DELETED_MESSAGES_FILTERS, G)
    async def _all(app: Client, msg: types.Message):
        global messages
        try: messages[msg.chat.id][msg.id] = msg
        except KeyError: messages[msg.chat.id] = {msg.id: msg}

    @Client.on_deleted_messages(DELETED_MESSAGES_FILTERS, G)
    async def _del(app: Client, msgs):
        for msg in msgs:
            msg: types.Message
            try:
                sm = await app.send_message(DELETED_MESSAGES_CHAT_ID, code(msg))
                m = messages[msg.chat.id][msg.id]
                await sm.edit(code(msg) + a("link", f"t.me/{m.chat.username}"))
                MT = enums.MessageMediaType
                if md := m.media:
                    if md == MT.PHOTO:
                        await app.send_photo(
                            DELETED_MESSAGES_CHAT_ID,
                            m.photo.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.VIDEO:
                        await app.send_video(
                            DELETED_MESSAGES_CHAT_ID,
                            m.video.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.VOICE:
                        await app.send_voice(
                            DELETED_MESSAGES_CHAT_ID,
                            m.voice.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.ANIMATION:
                        await app.send_animation(
                            DELETED_MESSAGES_CHAT_ID,
                            m.animation.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.AUDIO:
                        await app.send_audio(
                            DELETED_MESSAGES_CHAT_ID,
                            m.audio.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.CONTACT:
                        await app.send_contact(
                            DELETED_MESSAGES_CHAT_ID,
                            phone_number=m.contact.phone_number,
                            first_name=m.contact.first_name,
                            last_name=m.contact.last_name,
                            vcard=m.contact.vcard,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.DICE:
                        dm = await app.send_dice(
                            DELETED_MESSAGES_CHAT_ID,
                            m.dice.emoji,
                            reply_to_message_id=sm.id
                        )
                        await app.send_message(
                            DELETED_MESSAGES_CHAT_ID,
                            "Результат игры другой чем в оригинале!",
                            reply_to_message_id=dm.id
                        )
                    elif md == MT.DOCUMENT:
                        await app.send_document(
                            DELETED_MESSAGES_CHAT_ID,
                            m.document.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.GAME:
                        await app.send_game(
                            DELETED_MESSAGES_CHAT_ID,
                            m.game.short_name,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.LOCATION:
                        await app.send_location(
                            DELETED_MESSAGES_CHAT_ID,
                            m.location.latitude,
                            m.location.longitude,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.POLL:
                        await app.send_poll(
                            DELETED_MESSAGES_CHAT_ID,
                            question=m.poll.question,
                            options=m.poll.options,
                            is_anonymous=m.poll.is_anonymous,
                            type=m.poll.type,
                            allows_multiple_answers=m.pool.allows_multiple_answers,
                            correct_option_id=m.pool.correct_option_id,
                            explanation=m.pool.explanation,
                            explanation_parse_mode=m.pool.explanation_parse_mode,
                            explanation_entities=m.pool.explanation_entities,
                            open_period=m.pool.open_period,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.STICKER:
                        await app.send_sticker(
                            DELETED_MESSAGES_CHAT_ID,
                            m.sticker.file_id,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.VENUE:
                        await app.send_venue(
                            DELETED_MESSAGES_CHAT_ID,
                            latitude=m.venue.latitude,
                            longitude=m.venue.longitude,
                            title=m.venue.title,
                            address=m.venue.address,
                            foursquare_id=m.venue.foursquare_id,
                            foursquare_type=m.venue.foursquare_type,
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.VIDEO_NOTE:
                        await app.send_sticker(
                            DELETED_MESSAGES_CHAT_ID,
                            m.video_note.file_id,
                            caption=m.caption.html if m.caption else '',
                            reply_to_message_id=sm.id
                        )
                    elif md == MT.WEB_PAGE:
                        # ватафак че это такое и как эту дрянь отправить
                        # TODO: Отловить эту хрень и посмотреть что это

                        # UPD: Это обычное сообщение с предпросмотром ссылки
                        await app.send_message(
                            DELETED_MESSAGES_CHAT_ID,
                            m.text.html,
                            reply_to_message_id=sm.id
                        )
                    else: print(md)

                else:
                    await app.send_message(
                        DELETED_MESSAGES_CHAT_ID,
                        m.text.html,
                        reply_to_message_id=sm.id
                    )
            except KeyError:
                pass
            except Exception as ex:
                print(__name__, ex)
                from traceback import print_exc
                print_exc()
                if str(ex) == "'NoneType' object has no attribute 'html'":
                    print(m)
else:
    print("config.DELETED_MESSAGES_CHAT_ID не задано. Удаленные сообщения регестрироваться не будут!")


        
@cmd(['online'])
async def _online(app, msg):
    await msg.edit(
        "<emoji id=5427009714745517609>✅</emoji> "
        "Теперь ты всегда в сети!\n"
        "Для отмены пиши " + code(PREFIX + 'offline')
    )
    await app.db.set("chat_tools", 'online', True)
    while await app.db.get("chat_tools", 'online', False):
        omsg = await app.send_message('me', '.')
        await omsg.delete()

        await asyncio.sleep(10)
   
@cmd(['offline'])
async def _offline(app, msg):
    await app.db.set('chat_tools', 'online', False)
    await msg.edit("<emoji id=5427009714745517609>✅</emoji> Теперь ты не в сети!")
