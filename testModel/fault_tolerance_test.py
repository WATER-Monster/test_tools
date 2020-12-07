import string
from config import PARAM_N
import requests
import json
import random
from utils.isNullCheck import is_null_check


allow_methods = ["GET", "POST"]
type_arr = ["str", "int", "map", "array", "float", "bool"]

class FaultToleranceTest:
    """
    接口级测试，数据边界测试，数据级测试，校验性测试
    注意在测试过程中应关闭token验证
    """
    def __init__(self, **kwargs):
        is_null_check(kwargs)
        self.api_url = kwargs.get("api_url")
        self.api_param = kwargs.get("api_param")
        self.api_methods = kwargs.get("api_methods")
        self.api_content_type = kwargs.get("api_content_type")

    @staticmethod
    def _request(**kwargs):
        m = getattr(requests, kwargs.get("methods").lower())
        if kwargs.get("methods") == "GET":
            res = m(kwargs.get("url"), kwargs.get("param"))
        elif kwargs.get("methods") == "POST":
            if kwargs.get("content_type") == "application/json":
                res = m(kwargs.get("url"), json.dumps(kwargs.get("param")), headers={"Content-Type": kwargs.get("content_type")})
            elif kwargs.get("content_type") == "application/x-www-form-urlencoded":
                res = m(kwargs.get("url"), kwargs.get("param"), headers={"Content-Type": kwargs.get("content_type")})
            else:
                res = m(kwargs.get("url"), kwargs.get("param"))
        return res.text

    def run(self):
        self._interface_test()
        self._data_type_test(PARAM_N)

    def _interface_test(self,):
        """
        https和http请求验证(未做)
        不同的methods验证
        :return:
        """
        for methods in allow_methods:
            res = self._request(url=self.api_url,methods=methods,param=self.api_param,content_type=self.api_content_type)
            print(res)

    def _data_type_test(self, n):
        """
        错误参数注入
        想法是针对每个参数都使用不同类型的随机值进行访问测试。但要把每个参数的每个类型都走一遍量太大了。
        走N次访问测试，每次都使用随机参数类型，只要N足够多，就能基本覆盖。
        :return:
        """
        for _ in range(n):
            param = {k:self._get_random_value() for k in self.api_param}
            res = self._request(url=self.api_url, param=param, methods=self.api_methods, content_type=self.api_content_type)
            print(param)
            print(res)

    @staticmethod
    def _get_random_value(t=None):
        case_map = {
            "int": random.randint(-2 ** 63, 2 ** 63 - 1),
            "float": random.uniform(-2 ** 63, 2 ** 63 - 1),
            "str": ''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))),
            "array": [''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))) for _ in
                      range(random.randint(0, 32))],
            "map": {''.join(random.sample(string.ascii_letters + string.digits, random.randint(0, 32))): ''.join(
                random.sample(string.ascii_letters + string.digits, random.randint(0, 32))) for _ in
                    range(random.randint(0, 64))},
            "bool": random.choice([True, False])
        }
        if t:
            ret = case_map.get(t)
        else:
            ret = case_map.get(random.choice(type_arr))
        return ret