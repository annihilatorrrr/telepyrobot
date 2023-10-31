import os
import random
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from telepyrobot import TMP_DOWNLOAD_DIRECTORY
from telepyrobot.utils.run_shell_cmnd import run_command


async def is_thumb_image_exists(file_name: str):
    thumb_image_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
    if os.path.exists(thumb_image_path):
        thumb_image_path = os.path.join(TMP_DOWNLOAD_DIRECTORY, "thumb_image.jpg")
    elif file_name is not None and file_name.lower().endswith(("mp4", "mkv", "webm")):
        metadata = extractMetadata(createParser(file_name))
        duration = metadata.get("duration").seconds if metadata.has("duration") else 0
        # get a random TTL from the duration
        ttl = str(random.randint(0, duration - 1))
        #
        thumb_image_path = gen_tg_thumbnail(await take_screen_shot(file_name, ttl))
    else:
        thumb_image_path = None
    return thumb_image_path


async def take_screen_shot(file_name: str, ttl: str) -> str:
    out_put_file_name = os.path.join(
        os.path.dirname(file_name), f"{ttl}_{str(time.time())}.jpg"
    )
    file_genertor_command = [
        "ffmpeg",
        "-ss",
        ttl,
        "-i",
        file_name,
        "-vframes",
        "1",
        out_put_file_name,
    ]
    stdout, stderr = await run_command(file_genertor_command)
    return out_put_file_name if os.path.lexists(out_put_file_name) else None


def gen_tg_thumbnail(downloaded_file_name: str) -> str:
    Image.open(downloaded_file_name).convert("RGB").save(downloaded_file_name)
    metadata = extractMetadata(createParser(downloaded_file_name))
    height = metadata.get("height") if metadata.has("height") else 0
    img = Image.open(downloaded_file_name)
    img.resize((320, height))
    img.save(downloaded_file_name, "JPEG")
    return downloaded_file_name
