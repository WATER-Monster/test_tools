import pandas
import os
from docOutput.docOutputInterface import DocOutputFactory


class ExcelOutput(DocOutputFactory):
    def write_line(self, **kwargs):
        pass

    def excel_exist(self):
        if not os.path.exists("ExcelOut"):
            os.mkdir("ExcelOut")
