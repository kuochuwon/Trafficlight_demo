

class Constant:
    CODE_TYPE_ISSUE_STATUS = 0
    CODE_TYPE_ISSUE_ERRORCODE = 1
    CODE_TYPE_REPORT_FROM = 2
    CODE_TYPE_DEVICE_STATUS = 3
    CODE_TYPE_DEVICE_COMPONENT = 4
    CODE_TYPE_EVENT_CATEGORY = 5
    CODE_TYPE_ISSUE_PRIORITY = 6

    COMMAND_DIMMING = 0
    COMMAND_POWER = 1
    COMMAND_DEVICE_TYPE_DEVICE = 0
    COMMAND_DEVICE_TYPE_GROUP = 1
    COMMAND_STATUS_RECEIVED = 0
    COMMAND_STATUS_QUEUE = 1

    CODE_EVENT_COMPONENT = {0: "CONTROLLER",
                            1: "LED"}

    CODE_EVENT_CATEGORY = {0: "溫度",
                           1: "濕度",
                           2: "電壓",
                           3: "亮度",
                           4: "電流",
                           5: "功率因數",
                           6: "功率",
                           7: "流明",
                           8: "資訊(開關機、排程、dimming)",
                           9: "dimming",
                           10: "開關機"}

    CODE_STATUS = {"NORMAL": 0,
                   "DEBUG": 1,
                   "INFO": 2,
                   "WARNING": 4,
                   "ERROR": 8,
                   "CRITICAL": 16}
    # User Role code
    SYSTEM_ADMIN = 1
    CUSTOMER_ADMIN = 2
    VENDOR_ADMIN = 3
    VENDOR_USER = 4

    ADMIN = "admin"
    REPORT_FROM_PEOPLE = "people"
    ISSUE_CHANGE_DESC = "status changed"
    DEFAULT_ISSUE_STATUS = "new"

    ACCESS_PRIVILEGES = {
        SYSTEM_ADMIN: [
            "new", "assigned", "in-progress", "resolved", "closed"
        ],
        CUSTOMER_ADMIN: [
            "new", "assigned", "in-progress", "resolved", "closed"
        ],
        VENDOR_ADMIN: [
            "assigned", "in-progress", "resolved", "closed"
        ],
        VENDOR_USER: [
            "in-progress"
        ]
    }

    PRIORITY_DUE_DAY = {
        "normal": 7,
        "high": 5,
        "urgent": 3
    }

    # for batch inset database in command view
    BATCH_COUNT_EXECUTE = 100

    # Redis related constants
    REDIS_EXPIRE_TIMES = 604800  # 60*60*24*7 == 604800 secs == 7 days


__code_table_name = {
    Constant.CODE_TYPE_ISSUE_STATUS: "issue_status",
    Constant.CODE_TYPE_ISSUE_ERRORCODE: "issue_errorcode",
    Constant.CODE_TYPE_REPORT_FROM: "report_from",
    Constant.CODE_TYPE_DEVICE_STATUS: "device_status",
    Constant.CODE_TYPE_DEVICE_COMPONENT: "device_component",
    Constant.CODE_TYPE_EVENT_CATEGORY: "event_category",
    Constant.CODE_TYPE_ISSUE_PRIORITY: "issue_priority"
}


def map_component(code):
    return Constant.CODE_EVENT_COMPONENT[code]


def map_category(code):
    return Constant.CODE_EVENT_CATEGORY[code]


def map_status(code_name):
    return Constant.CODE_STATUS[code_name]


def get_codes_name(code_type):
    return __code_table_name[code_type]
