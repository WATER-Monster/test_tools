from fileParser.markDown import MarkDownParser
from testModel.functionTest import FunctionTest
from testModel.stressTest import StressTest
from testModel.fault_tolerance_test import FaultToleranceTest
from docOutput.textOutput import TextOutput


def run_test(file_path, is_func_test=True, is_stress_test=True, fault_test=True):
    api_lists = MarkDownParser.read(file_path)
    for api in api_lists:
        if not isinstance(api, dict):
            raise TypeError("api params should be a dict")
        if is_func_test:
            f = FunctionTest()
            f_t_response = f.run(**api)
            t = TextOutput(**api)
            t.out_put(f_t_response)
        # if is_stress_test:
        #     s = StressTest(**api)
        #     s_t_response = s.run()
        # if fault_test:
        #     f = FaultToleranceTest(**api)
        #     f.run()


if __name__ == '__main__':
    run_test("back_end_doc.md")