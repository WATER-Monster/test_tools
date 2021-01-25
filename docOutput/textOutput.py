import datetime
import os
from docOutput.docOutputInterface import DocOutputFactory


class TextOutput(DocOutputFactory):
    def write_line(self, **kwargs):
        self.out_put(**kwargs)
        if not os.path.exists("TextOut"):
            os.mkdir("TextOut")

        date = datetime.datetime.now().strftime("%Y-%m-%d %H")
        text_path = "TextOut/%s.text" % date

        def get_dict(dict1):
            s = ""
            for key,val in dict1.items():
                s+=key+(" "*(12-len(key) if len(key)<=12 else 0))+": "
                try:
                    s+=str(val).encode().decode("unicode_escape")+"\n"
                except Exception:
                    s += str(val) + "\n"
            return s

        with open(text_path, "a+", encoding="UTF-8") as f:
            f.write("TestName    : "+self.test_name+"\n"+
                    "Url         : "+self.api_url+"\n"+
                    "Param       : "+str(self.api_param)+"\n"+
                    "Method      : "+self.api_methods+"\n"+
                    "Content-Type: "+(self.api_content_type if self.api_content_type else "null")+"\n"+
                    get_dict(kwargs)+"\n\n")