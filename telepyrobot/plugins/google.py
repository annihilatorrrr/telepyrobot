import os
import time
import asyncio
import requests
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Search for a query on google using userbot!

`{COMMAND_HAND_LER}gs <query>`
"""


@TelePyroBot.on_message(filters.command("gs", COMMAND_HAND_LER) & filters.me)
async def google_s(c: TelePyroBot, m: Message):
    input_str = m.text.split(None, 1)[1]
    sample_url = f'https://da.gd/s?url=https://lmgtfy.com/?q={input_str.replace(" ", "+")}%26iie=1'
    if response_api := requests.get(sample_url).text:
        await m.edit_text(
            f"[{input_str}]({response_api.rstrip()})\n`Thank me Later 🙃` "
        )
    else:
        await m.edit_text("`Something is wrong. please try again later.``")
    return
