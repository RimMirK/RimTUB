# import asyncio

# import openai
# # from openai import exceptions # FIXME
# from pyrogram.types import Message
# from pyrogram import Client

# from utils import Cmd, get_group, Module, Argument as Arg, helplist, Command
# from utils.scripts import get_args_raw

# from typing import Union

# cmd = Cmd(get_group())

# @cmd(["gpt", "rgpt"])
# async def chatpgt(app: Client, message: Message):
#     if message.command[0] == "rgpt":
#         args = get_args_raw(message, use_reply=True)
#     else:
#         args = get_args_raw(message)

#     if not args:
#         return await message.reply(
#             "<emoji id=5260342697075416641>❌</emoji><b> You didn't ask a question GPT</b>",
#             quote=True,
#         )

#     api_key = await app.db.get("ChatGPT", "api_key")
#     if not api_key:
#         return await message.reply(
#             "<emoji id=5260342697075416641>❌</emoji><b> You didn't provide an api key for GPT</b>",
#             quote=True,
#         )

#     openai.api_key = api_key

#     data: dict = await app.db.get(
#         "ChatGPT",
#         f"gpt_id{message.chat.id}",
#         {
#             "enabled": True,
#             "gpt_messages": [],
#         },
#     )

#     if not data.get("enabled"):
#         return await message.reply(
#             "<emoji id=5260342697075416641>❌</emoji><b> GPT is not available right now</b>",
#             quote=True,
#         )

#     data["enabled"] = False
#     await app.db.set("ChatGPT", f"gpt_id{message.chat.id}", data)

#     msg = await message.reply(
#         "<emoji id=5443038326535759644>💬</emoji><b> GPT is generating response, please wait</b>",
#         quote=True,
#     )
#     try:
#         completion = await openai.ChatCompletion.acreate(
#             model="gpt-3.5-turbo",
#             messages=data["gpt_messages"] + [{"role": "user", "content": args}],
#         )
#     # except exceptions.RateLimitError: # FIXME
#     #     data["enabled"] = True
#     #     await app.db.set("ChatGPT", f"gpt_id{message.chat.id}", data)
#     #     return await msg.edit_text(
#     #         "<emoji id=5260342697075416641>❌</emoji><b> Model is currently overloaded with other requests.</b>"
#     #     )
#     except Exception as e:
#         data["enabled"] = True
#         await app.db.set("ChatGPT", f"gpt_id{message.chat.id}", data)
#         return await msg.edit_text(
#             f"<emoji id=5260342697075416641>❌</emoji><b> Something went wrong: {e}</b>"
#         )

#     response = completion.choices[0].message.content

#     data["gpt_messages"].append({"role": "user", "content": args})
#     data["gpt_messages"].append({"role": completion.choices[0].message.role, "content": response})
#     data["enabled"] = True
#     await app.db.set("ChatGPT", f"gpt_id{message.chat.id}", data)

#     await msg.edit_text(response, parse_mode=enums.ParseMode.MARKDOWN)


# @cmd(["gptst"])
# async def chatpgt_set_key(app: Client, message: Message):
#     args = get_args_raw(message)

#     if len(message.text.split()) < 1:
#         return await message.edit("<emoji id=5260342697075416641>❌</emoji><b> You didn't provide an api key</b>")
    
#     await app.db.set("ChatGPT", "api_key", args)
#     await message.edit_text(
#         "<emoji id=5260726538302660868>✅</emoji><b> You set api key for GPT</b>"
#     )


# @cmd(["gptcl"])
# async def chatpgt_clear(app: Client, message: Message):
#     await app.db.remove("ChatGPT", f"gpt_id{message.chat.id}")

#     await message.edit_text(
#         "<emoji id=5258130763148172425>✅</emoji><b> You cleared messages context</b>"
#     )


# module = Module("chatgpt", author='@KurimuzonAkuma')

# module.add_command(Command("gpt", [Arg('query')], "Ask ChatGPT"))
# module.add_command(Command("rgpt", [Arg('reply')], "Ask ChatGPT from replied message"))
# module.add_command(Command("gptst", [Arg('api key')], "Set GPT api key"))
# module.add_command(Command("gptcl", [], "Clear GPT messages context"))

# helplist.add_module(module)