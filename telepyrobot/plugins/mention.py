import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER
from telepyrobot.utils.parser import mention_markdown

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Generate a  hyperlink/permanent link for a profile.

**Mention**
Usage:
`{COMMAND_HAND_LER}mention <custom text> <username without @>`
or
`{COMMAND_HAND_LER}mention <custom text> <user_id>`
"""


@TelePyroBot.on_message(filters.command("mention", COMMAND_HAND_LER) & filters.me)
async def mention(c: TelePyroBot, m: Message):
    args = m.text.split(None, 2)
    if len(args) == 3:
        name = args[1]
        user = args[2]
        if isinstance(user, int):
            rep = f"{mention_markdown(name, user)}"
        else:
            rep = f'<a href="tg://resolve?domain={name}">{user}</a>'
        await m.edit_text(rep, disable_web_page_preview=True, parse_mode="html")
    else:
        await m.edit_text(
            f"Check `{COMMAND_HAND_LER}help {__PLUGIN__}` for infor on how to use",
            parse_mode="md",
        )
        return
