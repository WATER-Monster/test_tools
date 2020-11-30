from isNullCheck import is_null_check
import requests
import json


class FunctionTest:
    @staticmethod
    def run(**kwargs):
        is_null_check(kwargs)
        methods = kwargs.get("api_methods")

        if methods == "GET":
            response = requests.get(kwargs.get("api_url"))
        elif methods == "POST":
            response = requests.post(kwargs.get("api_url"),
                                     data=json.dumps(kwargs.get("api_param")),
                                     headers={"Content-Type":kwargs.get("api_content_type")})
        else:
            raise Exception("methods type do not support")

        # 对比response和文档中提取出的正确回参和错误回参
        doc_true_response = {key:value for key, value in kwargs.get("api_res_true").items()}
        doc_false_response = {key:value for key, value in kwargs.get("api_res_false").items()}

        is_correct = False

        #  TODO 非暴力比对
        if response.status_code == 200:
            pass

        return {
            "api_name": kwargs.get("api_name"),
            "is_correct": is_correct,
            "status": response.status_code,
            "resp":response.content
        }

    def _compare_response(self):
        pass
