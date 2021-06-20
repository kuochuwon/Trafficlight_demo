from app.main import db
from app.main.log import logger
from app.main.model.user import sdUser
from app.main.model.customer import sdCustomer
from app.main.model.device_model import sdDeviceModel


def seed():
    # Add system customer
    logger.debug("Adding system customer")
    sys_cust = db.session.query(sdCustomer).filter(sdCustomer.id == 0).first()
    if sys_cust:
        logger.debug("System customer existed, ignore")
    else:
        sys_cust = sdCustomer(id=0,
                              name="system",
                              display_name="System",
                              comment="System (Default)")
        db.session.add(sys_cust)

    # Add system administrator
    logger.debug("Adding system administrator")
    sys_user = db.session.query(sdUser).filter(sdUser.id == 0).first()
    if sys_user:
        logger.debug("System administrator existed, ignore")
    else:
        sys_cust.users.append(sdUser(id=0,
                                     name="admin",
                                     display_name="System Administrator",
                                     password="AcBel.Lighting,168",
                                     comment="System Administrator (Default)"))

    # Add default device_model
    logger.debug("Adding default device model")
    default_model = db.session.query(sdDeviceModel).filter(sdDeviceModel.id == 0).first()
    if default_model:
        logger.debug("Default device model existed, ignore")
    else:
        default_model = sdDeviceModel(id=0,
                                      name="DEFAULT",
                                      display_name="Default Model for all device model")
        db.session.add(default_model)

    # Commit transaction
    db.session.commit()
