from fileParser.markDown import MarkDownParser
from testModel.functionTest import FunctionTest


def run_test(file_path, **kwargs):
    api_lists = MarkDownParser.read(file_path)
    for api in api_lists:
        if not isinstance(api, dict):
            raise TypeError("api params should be a dict")
        f_t_response = FunctionTest.run(**api)
        print(f_t_response)


if __name__ == '__main__':
    run_test("back_end_doc.md")