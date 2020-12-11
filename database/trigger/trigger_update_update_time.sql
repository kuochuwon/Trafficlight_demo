CREATE OR REPLACE FUNCTION trigger_update_update_time()
RETURNS TRIGGER AS $$
BEGIN
  NEW.update_time = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

