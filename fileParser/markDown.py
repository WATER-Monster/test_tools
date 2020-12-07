from utils.encodingFactory import EncodingFactory
from config import *
import re


class MarkDownParser:
    @staticmethod
    def read(file_path):
        file_str = EncodingFactory.file_reader(file_path)
        api_list = file_str.split("----")

        format_api_param_lists = list()

        for fs in api_list:
            try:
                api_name = re.search(API_NAME_PATTERN, fs)
                api_url = re.search(API_URL_PATTERN, fs)
                api_methods = re.search(API_METHODS_PATTERN, fs)
                api_content_type = re.search(API_CONTENT_TYPE, fs)
                #  TODO 用正则通用过滤掉，兼容各类写法
                api_param = re.search(API_PARAM, fs, re.DOTALL).group(1).replace("\n", "").replace("```", "").replace("json", "")
                api_res_true = re.search(API_RES_TRUE, fs, re.DOTALL).group(1).replace("\n", "").replace("```", "").replace("json", "")
                api_res_false = re.search(API_RES_FALSE, fs, re.DOTALL).group(1).replace("\n", "").replace("```", "").replace("json", "")

                format_api_param_lists.append({
                    "api_name":api_name.group(1),
                    "api_url":api_url.group(1),
                    "api_methods":api_methods.group(1),
                    "api_content_type":api_content_type.group(1) if api_methods.group(1) == "POST" else "",
                    "api_param":eval(api_param),
                    "api_res_true":eval(api_res_true),
                    "api_res_false":eval(api_res_false)
                })
            except Exception:
                continue

        return format_api_param_lists
