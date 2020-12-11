from app.main.constant import get_codes_name
from app.main.log import logger
from app.main.model.code import sdCode
from app.main.model.customer import sdCustomer
from app.main.util.conv import datetime_to_iso8601


def get_api_routes(app):
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)


def get_codes(cust_id):
    try:
        customer = sdCustomer.search_cust(cust_id)
        # if customer return false, means vendor, vendor should follow customer's code format
        if not customer:
            vendor = sdCustomer.search_cust_obj(cust_id)
            cust_id = vendor.cust_id

        codes = sdCode.get_codes(cust_id)
        if not codes:
            return None

        codes_table = {}
        for code in codes:
            # TAG change str here
            codes_table.setdefault(get_codes_name(code.code_type), [])\
                .append(dict(id=str(code.id),
                             name=code.name,
                             display_name=code.display_name,
                             create_time=datetime_to_iso8601(code.create_time),
                             update_time=datetime_to_iso8601(code.update_time)))

        response = dict(codes_table=codes_table)
        return response
    except Exception as e:
        logger.error(f"The user input may incorrect, {str(e)}")
        raise
