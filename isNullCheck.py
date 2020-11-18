
# TODO GET 和 POST 的参数不同
def is_null_check(check_dict):
    if not isinstance(check_dict, dict):
        raise TypeError("this function should accept a dict, not %s" % type(check_dict))
    for item in check_dict:
        if check_dict.get(item) is None:
            raise TypeError("%s should not be None" % item)