API_NAME_PATTERN = r"###(.*)"
API_URL_PATTERN = r"> \*\*url:[\s*]?(.*)[\s*]?\*\*"
API_METHODS_PATTERN = r"> \*\*[\s*]?methods:[\s*]?(.*)[\s*]?\*\*"
API_CONTENT_TYPE = r"> \*\*[\s*]?Content-Type:[\s*]?(.*)[\s*]?\*\*"
API_PARAM = r"\[//\]:[\s*]?param\n```\w+(.*)```\n\[//\]:[\s*]?param"
API_RES_TRUE = r"\[//\]:[\s*]?True-response\n```\w+(.*)```\n\[//\]:[\s*]?True-response"
API_RES_FALSE = r"\[//\]:[\s*]?False-response\n```\w+(.*)```\n\[//\]:[\s*]?False-response"

PARAM_N = 10 # 容错测试中循环次数

SQL_INJECTION_ARRAY = [
    "'",
    "N/A",
    "' OR '1' = '1",
    "') OR ('1' = '1",
    "value' OR '1' = '2",
    "value') OR ('1' = '2",
    "' AND '1' = '2",
    "') AND ('1' = '2",
    "' OR 'ab' = 'a''b",
    "') OR ('ab' = 'a''b"
]

SPECIAL_CHAR_ARRAY = [
    "'",
    '"',
    ".",
    ",",
    "`",
    "~",
    "(",
    ")",
    "{",
    "}",
    "^",
    "%",
    "\\",
    "/",
    "\n",
    "\t"
]