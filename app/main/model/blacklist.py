from sqlalchemy.sql import func

from app.main import db


class sdBlacklistToken(db.Model):
    __tablename__ = "sd00_blacklist_tokens"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False, comment="JWT refresh token")
    create_time = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment="Create time")

    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"<sdBlacklistToken id={self.id}/token={self.token}/create_time={self.create_time}>"

    @staticmethod
    def check_is_in_blacklist(token_hex):
        res = sdBlacklistToken.query.filter_by(token=token_hex).first()
        return True if res else False

    @staticmethod
    def revoke_token(token):
        blacklist_token = sdBlacklistToken(token=token)
        return blacklist_token
