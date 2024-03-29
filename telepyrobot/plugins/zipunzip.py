import shutil
import os
from telepyrobot.setclient import TelePyroBot
from pyrogram import filters
from pyrogram.types import Message
from telepyrobot import COMMAND_HAND_LER

__PLUGIN__ = os.path.basename(__file__.replace(".py", ""))

__help__ = f"""
Zip/Unzip operations using your Userbot!

`{COMMAND_HAND_LER}zip <folder>` to zip the folder.
`{COMMAND_HAND_LER}unzip <file>` to unzip the file.
"""


async def zipdir(path):
    if path.endswith("/"):
        path = path[:-1]
    filename = path.split("/")[-1]
    shutil.make_archive(filename, "zip", path)
    return f"{filename}.zip"


async def unzipfiles(zippath):
    foldername = zippath.split("/")[-1]
    extract_path = f"/root/telepyrobot/cache/unzip/{foldername}"
    shutil.unpack_archive(zippath, extract_path)
    return extract_path


@TelePyroBot.on_message(filters.command("zip", COMMAND_HAND_LER) & filters.me)
async def zipit(c: TelePyroBot, m: Message):

    if (m.command) == 1:
        await m.edit_text("Please enter a directory path to zip!")
        return

    location = m.text.split(None, 1)[1]
    await m.edit_text("<code>Zipping file...</code>")
    filename = await zipdir(location)
    await m.edit_text(
        f"File zipped and saved to <code>/root/{filename}</code>, to upload, use <code>{COMMAND_HAND_LER}upload {filename}</code>"
    )
    return


@TelePyroBot.on_message(filters.command("unzip", COMMAND_HAND_LER) & filters.me)
async def unzipit(c: TelePyroBot, m: Message):

    if (m.command) == 1:
        await m.edit_text("Please enter path to zip file which you want to extract!")
        return

    fileLoc = m.text.split(None, 1)[1]
    await m.edit_text("<code>Unzipping file...</code>")
    extract_path = await unzipfiles(fileLoc)
    await m.edit_text(f"Files unzipped to <code>{extract_path}</code>.")
    return
