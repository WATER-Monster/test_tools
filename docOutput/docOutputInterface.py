import abc


class DocOutputFactory(metaclass=abc.ABCMeta):
    def __init__(self,date, **kwargs):
        self.date = date
        self.api_url = kwargs.get("api_url")
        self.api_param = kwargs.get("api_param")
        self.api_methods = kwargs.get("api_methods")
        self.api_content_type = kwargs.get("api_content_type")
        self.test_name = kwargs.get("api_test_name")

    def out_put(self, **kwargs):
        def get_dict(dict1):
            s = ""
            for key,val in dict1.items():
                if key == "Param" or key == "Method" or key == "Content-Type":
                    continue
                s+="\033[0;31m"+key+(" "*(12-len(key) if len(key)<=12 else 0))+": \033[0m"
                try:
                    s+=str(val).encode().decode("unicode_escape")+"\n"
                except Exception:
                    s += str(val) + "\n"
            return s

        print("\033[1;31mTestName    : "+self.test_name + "\033[0m",
              "\033[0;31mUrl         : "+self.api_url + "\033[0m",
              "\033[0;31mParam       : \033[0m"+(str(self.api_param) if kwargs.get("Param") is None else str(kwargs.get("Param"))),
              "\033[0;31mMethod      : \033[0m"+(self.api_methods if kwargs.get("Method") is None else kwargs.get("Method")),
              "\033[0;31mContent-Type: \033[0m"+((self.api_content_type if self.api_content_type else "null") if kwargs.get("Content-Type") is None else kwargs.get("Content-Type")),
              get_dict(kwargs),
              sep="\n")

    @abc.abstractmethod
    def write_line(self):
        pass