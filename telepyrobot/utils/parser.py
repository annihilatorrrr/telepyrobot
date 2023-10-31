import html
import re


def cleanhtml(raw_html):
    cleanr = re.compile("<.*?>")
    return re.sub(cleanr, "", raw_html)


def escape_markdown(text):
    escape_chars = r"\*_`\["
    return re.sub(f"([{escape_chars}])", r"\\\1", text)


def mention_html(user_id, name):
    return f'<a href="tg://user?id={user_id}">{html.escape(name)}</a>'


def mention_markdown(name, user_id):
    return f"[{escape_markdown(name)}](tg://user?id={user_id})"
