from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import logging
import asyncio
from datetime import datetime
from pyrogram.enums import ChatMemberStatus
from dotenv import load_dotenv
from os import environ
import os
import time
from status import format_progress_bar
from video import download_video, upload_video
from web import keep_alive

load_dotenv('config.env', override=True)

logging.basicConfig(level=logging.INFO)

api_id = os.environ.get('TELEGRAM_API', '')
if len(api_id) == 0:
    logging.error("TELEGRAM_API variable is missing! Exiting now")
    exit(1)

api_hash = os.environ.get('TELEGRAM_HASH', '')
if len(api_hash) == 0:
    logging.error("TELEGRAM_HASH variable is missing! Exiting now")
    exit(1)
    
bot_token = os.environ.get('BOT_TOKEN', '')
if len(bot_token) == 0:
    logging.error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)
dump_id = os.environ.get('DUMP_CHAT_ID', '')
if len(dump_id) == 0:
    logging.error("DUMP_CHAT_ID variable is missing! Exiting now")
    exit(1)
else:
    dump_id = int(dump_id)

fsub_id = os.environ.get('FSUB_ID', '')
if len(fsub_id) == 0:
    logging.error("FSUB_ID variable is missing! Exiting now")
    exit(1)
else:
    fsub_id = int(fsub_id)

app = Client("TeraBox_Leech_Group", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    sticker_message = await message.reply_sticker("CAACAgIAAxkBAAEYonplzwrczhVu3I6HqPBzro3L2JU6YAACvAUAAj-VzAoTSKpoG9FPRjQE")
    await asyncio.sleep(2)
    await sticker_message.delete()
    user_mention = message.from_user.mention
    reply_message = f"ᴡᴇʟᴄᴏᴍᴇ, {user_mention}.\n\n🌟 ɪ ᴀᴍ ᴀ ᴛᴇʀᴀʙᴏx ᴅᴏᴡɴʟᴏᴀᴅᴇʀ ʙᴏᴛ. sᴇɴᴅ ᴍᴇ ᴀɴʏ ᴛᴇʀᴀʙᴏx ʟɪɴᴋ ɪ ᴡɪʟʟ ᴅᴏᴡɴʟᴏᴀᴅ ᴡɪᴛʜɪɴ ғᴇᴡ sᴇᴄᴏɴᴅs ᴀɴᴅ sᴇɴᴅ ɪᴛ ᴛᴏ ʏᴏᴜ ✨."
    join_button = InlineKeyboardButton("𝙂𝙍𝙊𝙐𝙋 ❤️‍🔥", url="https://t.me/PBX1_BOTS")
    developer_button = InlineKeyboardButton("𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝙍 😎", url="https://t.me/PBX1_OP")
    reply_markup = InlineKeyboardMarkup([[join_button, developer_button]])
    await message.reply_text(reply_message, reply_markup=reply_markup)

async def is_user_member(client, user_id):
    try:
        member = await client.get_chat_member(fsub_id, user_id)
        logging.info(f"User {user_id} membership status: {member.status}")
        if member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Error checking membership status for user {user_id}: {e}")
        return False

@app.on_message(filters.text)
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    is_member = await is_user_member(client, user_id)

    if not is_member:
        join_button = InlineKeyboardButton("𝙂𝙍𝙊𝙐𝙋 ❤️‍🔥", url="https://t.me/PBX1_BOTS")
        reply_markup = InlineKeyboardMarkup([[join_button]])
        await message.reply_text("𝙔𝙤𝙪 𝙈𝙪𝙨𝙩 𝙅𝙤𝙞𝙣 𝙈𝙮 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙏𝙤 𝙐𝙨𝙚 𝙈𝙚 😁", reply_markup=reply_markup)
        return

    terabox_link = message.text.strip()
    if "terabox" not in terabox_link:
        await message.reply_text("𝙋𝙡𝙚𝙖𝙨𝙚 𝙎𝙚𝙣𝙙 𝘼 𝙑𝙖𝙡𝙞𝙙 𝙏𝙚𝙧𝙖𝘽𝙤𝙭 𝙇𝙞𝙣𝙠")
        return

    reply_msg = await message.reply_text("𝙎𝙚𝙣𝙙𝙞𝙣𝙜 𝙔𝙤𝙪 𝙏𝙝𝙚 𝙈𝙚𝙙𝙞𝙖...🤤")

    try:
        file_path, thumbnail_path, video_title = await download_video(terabox_link, reply_msg, user_mention, user_id)
        await upload_video(client, file_path, thumbnail_path, video_title, reply_msg, dump_id, user_mention, user_id, message)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await reply_msg.edit_text("𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 𝙁𝙖𝙞𝙡𝙙 ❗️ 𝙈𝙖𝙮 𝘽𝙚 𝘿𝙪𝙚 𝙏𝙤 𝙁𝙞𝙡𝙚 𝙎𝙞𝙯𝙚 𝙊𝙧 𝙈𝙪𝙡𝙩𝙞𝙥𝙡𝙚 𝙑𝙞𝙙𝙚𝙤 𝙄𝙣 𝙏𝙝𝙚 𝙇𝙞𝙣𝙠 𝙏𝙧𝙮 𝘼𝙣𝙤𝙩𝙝𝙚𝙧 𝙇𝙞𝙣𝙠 👍")

if __name__ == "__main__":
    keep_alive()
    app.run()
