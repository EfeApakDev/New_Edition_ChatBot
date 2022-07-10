import re
import os
from asyncio import gather, get_event_loop, sleep

from aiohttp import ClientSession
from pyrogram import Client, filters, idle
from Python_ARQ import ARQ

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import pyrogram
from Config import Config
from datetime import datetime

is_config = os.path.exists("config.py")

if is_config:
    from config import *
else:
    from sample_config import *

sakir = Client(
    ":memory:",
    bot_token=bot_token,
    api_id=6,
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e",
)
# şimdi bak karşim bu botu @sakirbey1 yazdı uzaaaaa
bot_id = int(bot_token.split(":")[0])
arq = None


async def sakirQuery(query: str, user_id: int):
    query = (
        query
        if LANGUAGE == "tr"
        else (await arq.translate(query, "tr")).result.translatedText
    )
    resp = (await arq.sakir(query, user_id)).result
    return (
        resp
        if LANGUAGE == "tr"
        else (
            await arq.translate(resp, LANGUAGE)
        ).result.translatedText
    )


async def type_and_send(message):
    chat_id = message.chat.id
    user_id = message.from_user.id if message.from_user else 0
    query = message.text.strip()
    await message._client.send_chat_action(chat_id, "typing")
    response, _ = await gather(sakirQuery(query, user_id), sleep(2))
    await message.reply_text(response)
    await message._client.send_chat_action(chat_id, "cancel")


@sakir.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[GitHub](nolur.com)"
        + " | [Group](t.me/SakirBey2)",
        disable_web_page_preview=True,
    )


@sakir.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await sleep(2)
    await message.reply_text("/repo - Get Repo Link")

    
@sakir.on_message(filters.new_chat_members, group=1)
async def hg(bot: Client, msg: Message):
    for new_user in msg.new_chat_members:
        if str(new_user.id) == str(Config.BOT_ID):
            await msg.reply(
                f'''`Hey` {msg.from_user.mention} `beni` {msg.chat.title} `grubuna eklediğin için teşekkürler⚡️`\n\n**Grublarda 10k yakın üye etiketleme özelliğim vardır komutlar için /help yazmanız yeterlidir✨**''')

        elif str(new_user.id) == str(Config.OWNER_ID):
            await msg.reply('İşte bu gelen benim sahibim.')
            
        # olm çalma kodları aq    
@sakir.on_message(filters.command("id"))
async def _id(_, message: Message):
    msg = message.reply_to_message or message
    out_str = "**User İnfo:**\n"
    out_str += f" ⚡️ __Grup ID__ : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f" 💎 __Yanıtlanan Kullanıcı Adı__ : {msg.from_user.first_name}\n"
    out_str += f" 💬 __Mesaj ID__ : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f" 🙋🏻‍♂️ __Yanıtlanan Kullanıcı ID__ : `{msg.from_user.id}`\n"
 
    await message.reply(out_str)

@sakir.on_message(filters.command("info"))
async def _id(_, message: Message):
    msg = message.reply_to_message or message
    out_str = "**User İnfo:**\n"
    out_str += f" ⚡️ __Grup ID__ : `{(msg.forward_from_chat or msg.chat).id}`\n"
    out_str += f" 💎 __Yanıtlanan Kullanıcı Adı__ : {msg.from_user.first_name}\n"
    out_str += f" 💬 __Mesaj ID__ : `{msg.forward_from_message_id or msg.message_id}`\n"
    if msg.from_user:
        out_str += f" 🙋🏻‍♂️ __Yanıtlanan Kullanıcı ID__ : `{msg.from_user.id}`\n"
 
    await message.reply(out_str)

@sakir.on_message(filters.command("ping"))
async def pingy(client, message):
    start = datetime.now()
    hmm = await message.reply("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await hmm.edit(
        f"█▀█ █▀█ █▄░█ █▀▀ █ \n█▀▀ █▄█ █░▀█ █▄█ ▄\n**Ping: {round(ms)}**")
  

@sakir.on_message(
    ~filters.private
    & filters.text
    & ~filters.command("help")
    & ~filters.edited,
    group=69,
)
async def chat(_, message):
    if message.reply_to_message:
        if not message.reply_to_message.from_user:
            return
        from_user_id = message.reply_to_message.from_user.id
        if from_user_id != bot_id:
            return
    else:
        match = re.search(
            "[.|\n]{0,}sakir[.|\n]{0,}",
            message.text.strip(),
            flags=re.IGNORECASE,
        )
        if not match:
            return
    await type_and_send(message)


@sakir.on_message(
    filters.private & ~filters.command("help") & ~filters.edited
)
async def chatpm(_, message):
    if not message.text:
        return
    await type_and_send(message)

# lan saaaaalğ
async def main():
    global arq
    session = ClientSession()
    arq = ARQ(ARQ_API_BASE_URL, ARQ_API_KEY, session)

    await sakir.start()
    print(
        """
------------------
| Herus Başladı!  |
------------------
"""
    )
    await idle()
# ok

loop = get_event_loop()
loop.run_until_complete(main())
