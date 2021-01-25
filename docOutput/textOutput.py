import os
from docOutput.docOutputInterface import DocOutputFactory


class TextOutput(DocOutputFactory):
    def write_line(self, **kwargs):
        self.out_put(**kwargs)
        if not os.path.exists("TextOut"):
            os.mkdir("TextOut")

        text_path = "TextOut/%s.text" % self.date

        def get_dict(dict1):
            s = ""
            for key,val in dict1.items():
                if key == "Param" or key == "Method" or key == "Content-Type":
                    continue
                s+=key+(" "*(12-len(key) if len(key)<=12 else 0))+": "
                try:
                    s+=str(val).encode().decode("unicode_escape")+"\n"
                except Exception:
                    s += str(val) + "\n"
            return s

        with open(text_path, "a+", encoding="UTF-8") as f:
            f.write("TestName    : "+self.test_name+"\n"+
                    "Url         : "+self.api_url+"\n"+
                    "Param       : "+(str(self.api_param) if kwargs.get("Param") is None else str(kwargs.get("Param")))+"\n"+
                    "Method      : "+(self.api_methods if kwargs.get("Method") is None else kwargs.get("Method"))+"\n"+
                    "Content-Type: "+((self.api_content_type if self.api_content_type else "null") if kwargs.get("Content-Type") is None else kwargs.get("Content-Type"))+"\n"+
                    get_dict(kwargs)+"\n\n")
