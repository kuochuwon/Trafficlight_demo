RET_OK = 0
RET_EXCEPTION = 1
RET_UNKNOWN = 2
RET_NO_PAYLOAD = 1000
RET_NOT_FOUND = 1001
RET_NO_CUST_ID = 1002
RET_AUTH_FAIL = 2000
RET_AUTH_MISSING = 2001
RET_AUTH_NO_CUST = 2002
RET_AUTH_NO_USER = 2003
RET_AUTH_WRONG_PASS = 2004
RET_AUTH_TOKEN_EXPIRED = 2005
RET_AUTH_TOKEN_MISSING = 2006

RET_AUTHO_FAIL = 2007
RET_AUTHO_ACCESS_FAIL = 2008
RET_AUTHO_STATUS_FAIL = 2009

code = {
    RET_OK: "OK",
    RET_EXCEPTION: "Exception",
    RET_UNKNOWN: "Unknown",
    RET_NO_PAYLOAD: "No payload",
    RET_NO_CUST_ID: "cust id not found",
    RET_NOT_FOUND: "No data found",
    RET_AUTH_FAIL: "Generic authentication fail",
    RET_AUTH_MISSING: "Missing customer name, user name, or password",
    RET_AUTH_NO_CUST: "Invalid customer name",
    RET_AUTH_NO_USER: "Invalid user name",
    RET_AUTH_WRONG_PASS: "Invalid user name or password",
    RET_AUTH_TOKEN_EXPIRED: "Token has expired",
    RET_AUTH_TOKEN_MISSING: "Missing token",
    RET_AUTHO_FAIL: "Generic authorization fail",
    RET_AUTHO_ACCESS_FAIL: "API access authorization fail",
    RET_AUTHO_STATUS_FAIL: "status update authorization fail"
}


def get_code_full(ret_code):
    return f"({ret_code}) {code.get(ret_code)}"


def get_code(ret_code):
    return code.get(ret_code) or code[RET_UNKNOWN]


def http_resp(ret_code, ret_hint=None, extra=None):
    try:
        ret = {"ret_code": ret_code, "ret_desc": code[ret_code]}
        if ret_hint:
            ret.update({"ret_hint": str(ret_hint)})
        if extra:
            ret.update(extra)
    except KeyError:
        return http_resp(RET_UNKNOWN, ret_code)
    return ret
