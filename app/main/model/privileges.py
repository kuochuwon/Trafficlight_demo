from app.main import db


class sdPrivilege(db.Model):
    __tablename__ = "sd17_privileges"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("sd18_roles.id"), nullable=False,
                        comment="authorization role, ex: admin, user")
    api_route = db.Column(db.Text, nullable=False, comment="API route, each api is unique")
