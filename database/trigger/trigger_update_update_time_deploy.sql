CREATE TRIGGER sd21_tr01 BEFORE UPDATE ON sd21_devices FOR EACH ROW EXECUTE PROCEDURE trigger_update_update_time();
CREATE TRIGGER sd22_tr01 BEFORE UPDATE ON sd22_device_groups FOR EACH ROW EXECUTE PROCEDURE trigger_update_update_time();
CREATE TRIGGER sd30_tr01 BEFORE UPDATE ON sd30_device_models FOR EACH ROW EXECUTE PROCEDURE trigger_update_update_time();
CREATE TRIGGER sd41_tr01 BEFORE UPDATE ON sd41_schedule_groups FOR EACH ROW EXECUTE PROCEDURE trigger_update_update_time();