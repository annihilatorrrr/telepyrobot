from sqlalchemy import Column, String, Boolean, UnicodeText
from telepyrobot import OWNER_ID
from telepyrobot.db import BASE, SESSION


class AFK(BASE):
    __tablename__ = "afk"
    user_id = Column(String(14), primary_key=True)
    is_afk = Column(Boolean, default=False)
    reason = Column(UnicodeText, default=False)

    def __init__(self, user_id, is_afk, reason):
        """initializing db"""
        self.user_id = str(user_id)
        self.is_afk = is_afk
        self.reason = reason

    def __repr__(self):
        """afk message for db"""
        return f"<AFK {self.user_id}>"


AFK.__table__.create(checkfirst=True)

MY_AFK = {}


def set_afk(afk, reason):
    global MY_AFK
    afk_db = SESSION.query(AFK).get(str(OWNER_ID))
    if afk_db:
        SESSION.delete(afk_db)
    afk_db = AFK(OWNER_ID, afk, reason)
    SESSION.add(afk_db)
    SESSION.commit()
    MY_AFK[OWNER_ID] = {"afk": afk, "reason": reason}


def get_afk():
    return MY_AFK.get(OWNER_ID)


def __load_afk():
    global MY_AFK
    try:
        qall = SESSION.query(AFK).all()
        MY_AFK = {int(x.user_id): {"afk": x.is_afk, "reason": x.reason} for x in qall}
    finally:
        SESSION.close()


__load_afk()
