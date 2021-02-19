import datetime
from fileParser.markDown import MarkDownParser
from testModel.functionTest import FunctionTest
from testModel.stressTest import StressTest
from testModel.fault_tolerance_test import FaultToleranceTest


def run_test(file_path, is_func_test=True, is_stress_test=True, fault_test=True):
    api_lists = MarkDownParser.read(file_path)
    print(api_lists, sep="\n")
    date = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    for api in api_lists:
        if not isinstance(api, dict):
            raise TypeError("api params should be a dict")
        if is_func_test:
            f = FunctionTest(date,**api)
            f.run()
        if is_stress_test:
            s = StressTest(date,**api)
            s.run()
        if fault_test:
            f = FaultToleranceTest(date,**api)
            f.run()


if __name__ == '__main__':
    run_test("back_end_doc.md")
    help()