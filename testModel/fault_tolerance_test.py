import string
import threading
from copy import deepcopy
from config import PARAM_N, SQL_INJECTION_ARRAY, SPECIAL_CHAR_ARRAY
import requests
import json
import random
from utils.isNullCheck import is_null_check
from concurrent.futures import ThreadPoolExecutor


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
        """
        枚举methods显得很蠢，但是好改
        :param kwargs:
        :return:
        """
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
        else:
            raise Exception("method not support")
        return res.text

    def run(self):
        self._interface_test()
        self._data_type_test(PARAM_N)
        self._sql_injection_test()

    def _interface_test(self):
        """
        接口级测试
        https和http请求验证(未做)
        不同的methods验证
        :return:
        """
        ret_list = list()
        for methods in allow_methods:
            res = self._request(url=self.api_url,methods=methods,param=self.api_param,content_type=self.api_content_type)
            ret_list.append(res)
        return ret_list

    def _data_type_test(self, n):
        """
        数据类型测试
        错误参数注入
        想法是针对每个参数都使用不同类型的随机值进行访问测试。但要把每个参数的每个类型都走一遍量太大了。
        走N次访问测试，每次都使用随机参数类型，只要N足够多，就能基本覆盖。
        :return:
        """
        ret_list = list()
        for _ in range(n):
            param = {k:self._get_random_value() for k in self.api_param}
            res = self._request(url=self.api_url, param=param, methods=self.api_methods, content_type=self.api_content_type)
            ret_list.append([param, res])
        return ret_list

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

    def _data_range_test(self):
        """
        数据边界测试
        目前只针对 str，int，float 类型进行测试，array和map如果要递归拆开再测试每个值的话，量太大了
        :return:
        """
        for param in self.api_param:
            self._data_range_factory(param)

    def _data_range_factory(self, param):
        # step1 空值测试
        # step2 极大值越界测试
        if isinstance(param, str):
            temp_param = deepcopy(self.api_param)
            temp_param[param] = ""
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)
            # string 的极大值理论可以无限大，做个极大的string参数输入实质算是服务器攻击了，这里跳过，
            # 但服务器编程时需要知道过大的request_body需要直接拦截掉，一般的框架都会有 MAX_CONTENT_LENGTH 之类的请求大小限制，也可以在Nginx做相关配置
            pass
        elif isinstance(param, int):
            temp_param = deepcopy(self.api_param)
            temp_param[param] = 0
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)
            temp_param[param] = 9223372036854775808 # 扔一个比__int64大1的值过去
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)
            temp_param[param] = 18446744073709551616 # 扔一个比unsigned__int64大1的值过去
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)
        elif isinstance(param, float):
            temp_param = deepcopy(self.api_param)
            temp_param[param] = float(0)
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)
            temp_param[param] = float("inf") # 扔一个float 64 的最大值。float("inf") 即float infinite。
            self._request(url=self.api_url, param=temp_param, methods=self.api_methods,
                          content_type=self.api_content_type)

    def _special_char_test(self):
        """
        str参数特殊字符测试
        :return:
        """
        for char in SPECIAL_CHAR_ARRAY:
            for param in self.api_param:
                if isinstance(param, str):
                    temp_param = deepcopy(self.api_param)
                    temp_param[param] += char
                    print(temp_param)
                    res = self._request(url=self.api_url,methods=self.api_methods,param=temp_param,content_type=self.api_content_type)
                    print(res)

    def _sql_injection_test(self):
        """
        sql注入测试
        :return:
        """
        for sql in SQL_INJECTION_ARRAY:
            for param in self.api_param:
                temp_param = deepcopy(self.api_param)
                temp_param[param] = sql
                print(temp_param)
                res = self._request(url=self.api_url,methods=self.api_methods,param=temp_param,content_type=self.api_content_type)
                print(res)

    def _concurrent_test(self, thread_count=10):
        """
        接口并发正确性测试
        在对重复提交会修改某一值的接口，用多线程并发请求，记录接口返回情况和并发线程数。
        :return:
        """
        count = 0
        while count <= thread_count:
            p = threading.Thread(self._request(url=self.api_url,methods=self.api_methods,param=self.api_param,content_type=self.api_content_type))
            p.start()
            count += 1
        return count