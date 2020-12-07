API_NAME_PATTERN = r"###(.*)"
API_URL_PATTERN = r"> \*\*url:[\s*]?(.*)[\s*]?\*\*"
API_METHODS_PATTERN = r"> \*\*[\s*]?methods:[\s*]?(.*)[\s*]?\*\*"
API_CONTENT_TYPE = r"> \*\*[\s*]?Content-Type:[\s*]?(.*)[\s*]?\*\*"
API_PARAM = r"\[//\]:[\s*]?param(.*)\[//\]:[\s*]?param"
API_RES_TRUE = r"\[//\]:[\s*]?True-response(.*)\[//\]:[\s*]?True-response"
API_RES_FALSE = r"\[//\]:[\s*]?False-response(.*)\[//\]:[\s*]?False-response"

PARAM_N = 10 # 容错测试中循环次数