from isNullCheck import is_null_check
import requests
import json


class FunctionTest:
    def __init__(self):
        self.doc_true_response = None
        self.doc_false_response = None
        self.response = None
        self.wrong_list = list()

    def run(self, **kwargs):
        is_null_check(kwargs)
        methods = kwargs.get("api_methods")

        if methods == "GET":
            self.response = requests.get(kwargs.get("api_url"))
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
                return self.response.text

        if len(self.wrong_list) == 0:
            is_correct = True

        return {
            "api_name": kwargs.get("api_name"),
            "is_correct": is_correct,
            "status": self.response.status_code,
            "wrong_list": self.wrong_list
        }

    # 递归json字典
    def _loop_dict(self, doc_t_r, response):
        if doc_t_r is None or response is None:
            return
        for item in doc_t_r:
            if isinstance(doc_t_r.get(item), dict):
                self._loop_dict(doc_t_r.get(item), response.get(item))
                continue
            if doc_t_r[item] == "no-need-confirm":
                continue
            if doc_t_r[item] != response[item]:
                self.wrong_list.append(item)
