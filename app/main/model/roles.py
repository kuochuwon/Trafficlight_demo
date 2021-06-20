from app.main import db


class sdRole(db.Model):
    __tablename__ = "sd18_roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, comment="authorization role, ex: admin, user")
    display_name = db.Column(db.String(50), comment="Display name")

    privileges = db.relationship("sdPrivilege", backref="role", lazy="dynamic")
    status_privileges = db.relationship("sdStatusPrivilege", backref="role", lazy="dynamic")
