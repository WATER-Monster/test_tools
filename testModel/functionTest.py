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
            self._loop_dict(self.doc_true_response)

            if len(self.wrong_list) == 0:
                is_correct = True

            return {
                "api_name": kwargs.get("api_name"),
                "is_correct": is_correct,
                "status": self.response.status_code,
                "wrong_list": self.wrong_list
            }

        return {
            "api_name": kwargs.get("api_name"),
            "is_correct": is_correct,
            "status": self.response.status_code
        }

    # TODO 记忆化递归
    def _loop_dict(self, doc_val, res_val, doc_key=None, res_key=None):
        for key, val in doc_val.items():
            if isinstance(val, dict):
                self._loop_dict(doc_val=val, doc_key=key)
                continue
            if val != "" and val != self.response.text.get(key):
                self.wrong_list.append({key: self.response.text.get(key)})
