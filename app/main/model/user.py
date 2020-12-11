from sqlalchemy.sql import func

from app.main import bcrypt, db
from app.main.constant import Constant


class sdUser(db.Model):
    __tablename__ = "sd11_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, comment="Name")
    display_name = db.Column(db.String(50), comment="Display name")
    comment = db.Column(db.Text, comment="Comment")
    status = db.Column(db.Integer, server_default="0", comment="Status")
    create_time = db.Column(db.DateTime, server_default=func.now(), comment="Create time")
    update_time = db.Column(db.DateTime, server_default=func.now(), comment="Update time")
    password_hash = db.Column("password", db.String(64), comment="Password")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")
    email = db.Column(db.String(100), comment="Email")
    telephone = db.Column(db.String(30), comment="Telephone number")
    line_id = db.Column(db.String(30), comment="LINE id")

    issue_logs = db.relationship("sdIssueLog", backref="user", lazy="dynamic")
    issues = db.relationship("sdIssue", backref="user", lazy="dynamic")

    __table_args__ = (db.UniqueConstraint("cust_id", "name"),)

    def __repr__(self):
        return f"<sdUser id={self.id}/name={self.name}/display_name={self.display_name}>"

    @property
    def password(self):
        raise AttributeError("password field cannot be read")

    @password.setter
    def password(self, new_password):
        self.password_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def search(cust_id, user_name):
        return sdUser.query.filter_by(cust_id=cust_id).filter_by(name=user_name).first()

    @staticmethod
    def getall(cust_id):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id).all()
        return users

    @staticmethod
    def getdetail(cust_id, user_list):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).all()
        return users

    @staticmethod
    def add(cust_id, name, display_name, password, email, telephone, comment):
        obj = sdUser()
        obj. cust_id = cust_id
        obj.name = name
        obj.display_name = display_name
        obj.password = password
        obj.email = email
        obj.telephone = telephone
        obj.comment = comment
        return obj

    # delete_all_user_groups: delete all user groups record corresponding to the user from m2m table
    @staticmethod
    def delete_all_user_groups(cust_id, user_list):
        users = db.session.query(sdUser).filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).all()
        for user in users:
            ug_rels = user.user_groups
            ug_rels.clear()

    @staticmethod
    def delete(cust_id, user_list):
        sdUser.query.filter(sdUser.cust_id == cust_id, sdUser.id.in_(user_list)).delete(synchronize_session=False)

    @staticmethod
    def update(cust_id, user_id, name, display_name, password, email, telephone, comment):
        obj = db.session.query(sdUser).filter(sdUser.id == user_id).first()
        if obj:
            if password:
                obj.password = password
            obj.name = name
            obj.display_name = display_name
            obj.email = email
            obj.telephone = telephone
            obj.comment = comment

        else:
            obj = sdUser()
            obj.cust_id = cust_id
            obj.name = name
            obj.display_name = display_name
            obj.password = password
            obj.email = email
            obj.telephone = telephone
            obj.comment = comment

        return obj

    @staticmethod
    def get_admin(cust_id):
        admin = db.session.query(sdUser).filter(sdUser.cust_id.in_(cust_id), sdUser.name == Constant.ADMIN).all()
        return admin
