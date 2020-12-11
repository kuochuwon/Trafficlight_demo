from app.main import db


class sdTodaySchedule(db.Model):
    __tablename__ = "sd62_today_schedules"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.String(5), comment="Time, SR+0, SS+0, 19:00")
    dimming = db.Column(db.Integer, comment="Dimming")
    device_id = db.Column(db.Integer, comment="Device_id")
    incre = db.Column(db.String(1), comment="Increase Light, y/n")
    vendor_device_id = db.Column(db.String(10), comment="Vender device id")

    def __repr__(self):
        return (
            f"<sdTodaySchedule id={self.id}/time={self.time}/dimming={self.dimming}"
            f"/device_id={self.device_id}/vender_device_id={self.vender_device_id}>"
        )
