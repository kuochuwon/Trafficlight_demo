from app.main import db


class sdGroupUser(db.Model):
    __tablename__ = "sd12_groupusers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")
    user_id = db.Column(db.Integer, db.ForeignKey("sd11_users.id"), comment="User or group id")

    __table_args__ = (db.UniqueConstraint("cust_id", "user_id"),)

    def __repr__(self):
        return f"<sdGroupUser id={self.id}/cust_id={self.cust_id}/user_id={self.user_id}>"
