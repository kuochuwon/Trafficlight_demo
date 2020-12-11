from sqlalchemy import exc

from app.main import db
from app.main.model.blacklist import sdBlacklistToken


def save_to_blacklist(token_hex):
    blacklist_token = sdBlacklistToken(token=token_hex)
    db.session.add(blacklist_token)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
