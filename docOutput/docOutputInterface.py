import abc
import pandas


class DocOutputFactory(metaclass=abc.ABCMeta):
    def __init__(self, **kwargs):
        self.api_url = kwargs.get("api_url")
        self.api_param = kwargs.get("api_param")
        self.api_methods = kwargs.get("api_methods")
        self.api_content_type = kwargs.get("api_content_type")

    def out_put(self, *args):
        print(self.api_url, self.api_param, self.api_methods, self.api_content_type, args, sep="\n")

    @abc.abstractmethod
    def write_line(self):
        pass