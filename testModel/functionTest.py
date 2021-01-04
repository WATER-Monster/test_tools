from docOutput.textOutput import TextOutput
from utils.isNullCheck import is_null_check
import requests
import json


class FunctionTest:
    def __init__(self, **kwargs):
        is_null_check(kwargs)
        self.api_url = kwargs.get("api_url")
        self.api_param = kwargs.get("api_param")
        self.api_methods = kwargs.get("api_methods")
        self.api_content_type = kwargs.get("api_content_type")

        self.doc_true_response = None
        self.doc_false_response = None
        self.response = None
        self.wrong_list = list()
        self.docOutput = TextOutput(api_test_name="FunctionTest",**kwargs)

    def run(self, **kwargs):
        methods = kwargs.get("api_methods")

        if methods == "GET":
            self.response = requests.get(kwargs.get("api_url"),params=kwargs.get("api_param"))
        elif methods == "POST":
            self.response = requests.post(kwargs.get("api_url"),
                                     data=json.dumps(kwargs.get("api_param")),
                                     headers={"Content-Type":kwargs.get("api_content_type")})
        else:
            raise Exception("methods type do not support")

        # 对比response和文档中提取出的正确回参和错误回参
        self.doc_true_response = {key:value for key, value in kwargs.get("api_res_true").items()}
        self.doc_false_response = {key:value for key, value in kwargs.get("api_res_false").items()}

        is_correct = False

        if self.response.status_code == 200:
            self._loop_dict(self.doc_true_response, json.loads(self.response.text))
        else:
            try:
                self._loop_dict(self.doc_false_response, json.loads(self.response.text))
            except Exception:
                self.docOutput.out_put(**{
                    "api_name": kwargs.get("api_name"),
                    "doc_correct": is_correct,
                    "msg": self.response.text,
                    "status": self.response.status_code,
                })
                return

        if len(self.wrong_list) == 0:
            is_correct = True

        self.docOutput.out_put(**{
            "api_name": kwargs.get("api_name"),
            "doc_correct": is_correct,
            "msg": self.response.text,
            "status": self.response.status_code,
            "wrong_list": self.wrong_list
        })

    # 递归json字典
    def _loop_dict(self, doc_t_r, response):
        if doc_t_r is None or response is None:
            return
        for item in doc_t_r:
            if isinstance(doc_t_r.get(item), dict):
                self._loop_dict(doc_t_r.get(item), response.get(item))
                continue
            if doc_t_r.get(item) == "no-need-confirm":
                continue
            if doc_t_r.get(item) != response.get(item):
                self.wrong_list.append({"key":item,
                                        "wrong_place":doc_t_r,
                                        "doc_value":doc_t_r.get(item),
                                        "response_value":response.get(item)})
