from app.main import db


class sdStatusPrivilege(db.Model):
    __tablename__ = "sd19_status_privileges"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey("sd18_roles.id"), nullable=False,
                        comment="authorization role, ex: admin, user")
    status_from = db.Column(db.Integer, comment="Current state")
    status_to = db.Column(db.Integer, comment="Next state")
    cust_id = db.Column(db.Integer, db.ForeignKey("sd10_customers.id"), comment="Customer id")

    @staticmethod
    def get_privilege(role_id, cust_id):
        obj = db.session.query(sdStatusPrivilege)\
            .filter(sdStatusPrivilege.role_id == role_id, sdStatusPrivilege.cust_id == cust_id).all()
        return obj
