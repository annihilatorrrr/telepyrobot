import re
import time


def replace_text(text):
    return (
        text.replace('"', "").replace("\\r", "").replace("\\n", "\n").replace("\\", "")
    )


async def extract_time(m, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]  # type: str
        if not time_num.isdigit():
            await m.reply("Unspecified amount of time.")
            return ""

        if unit == "m":
            bantime = int(time.time() + int(time_num) * 60)
        elif unit == "h":
            bantime = int(time.time() + int(time_num) * 60 * 60)
        elif unit == "s":
            bantime = int(time.time() + int(time_num) * 24 * 60 * 60)
        else:
            return ""
        return bantime
    else:
        await m.reply(
            f"Invalid time type specified. Needed m, h, or s. got: {time_val[-1]}"
        )
        return ""


async def extract_time_str(m, time_val):
    if any(time_val.endswith(unit) for unit in ("m", "h", "d")):
        unit = time_val[-1]
        time_num = time_val[:-1]
        if not time_num.isdigit():
            await m.reply("Unspecified amount of time.")
            return

        if unit == "m":
            bantime = int(int(time_num) * 60)
        elif unit == "h":
            bantime = int(int(time_num) * 60 * 60)
        elif unit == "s":
            bantime = int(int(time_num) * 24 * 60 * 60)
        else:
            return
        return bantime
    else:
        await m.reply(
            f"Invalid time type specified. Needed m, h, or s. got: {time_val[-1]}"
        )
        return


def make_time(time_val):
    if int(time_val) == 0:
        return "0"
    if int(time_val) <= 3600:
        bantime = f"{int(time_val / 60)}m"
    elif int(time_val) >= 3600 and time_val <= 86400:
        bantime = f"{int(time_val / 60 / 60)}h"
    elif int(time_val) >= 86400:
        bantime = f"{int(time_val / 24 / 60 / 60)}d"
    return bantime


def id_from_reply(m):
    prev_message = m.reply_to_message
    if not prev_message:
        return None, None
    user_id = m.from_user.id
    res = m.text.split(None, 1)
    return (user_id, "") if len(res) < 2 else (user_id, res[1])


def split_quotes(text: str):
    if not any(text.startswith(char) for char in START_CHAR):
        return text.split(None, 1)
    counter = 1
    while counter < len(text):
        if text[counter] == "\\":
            counter += 1
        elif text[counter] == text[0] or (
            text[0] == SMART_OPEN and text[counter] == SMART_CLOSE
        ):
            break
        counter += 1
    else:
        return text.split(None, 1)

    key = remove_escapes(text[1:counter].strip())
    rest = text[counter + 1 :].strip()
    if not key:
        key = text[0] + text[0]
    return list(filter(None, [key, rest]))


def extract_text(m):
    return m.text or m.caption or (m.sticker.emoji if m.sticker else None)


def remove_escapes(text: str) -> str:
    res = ""
    is_escaped = False
    for counter in range(len(text)):
        if is_escaped:
            res += text[counter]
            is_escaped = False
        elif text[counter] == "\\":
            is_escaped = True
        else:
            res += text[counter]
    return res
