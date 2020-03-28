from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig


class Data:
    def __init__(self, file_name, sheet_name):
        """
        使用Excel工具类，获取结果list
        :param file_name:
        :param sheet_name:
        """
        self.reader = ExcelReader(file_name, sheet_name)
        # print(self.reader)

    def get_run_data(self):
        """
        根据是否运行列 == y，获取执行测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == "y":
                # 3、保存要执行结果，放到新的列表
                run_list.append(line)
        # print(run_list)
        return run_list

    def get_case_list(self):
        """
        获取全部测试用例
        :return:
        """
        run_list = [line for line in self.reader.data()]
        return run_list

    def get_case_pre(self, pre):
        """
        获取全部测试用例后判断执行的用例
        :return:
        """
        run_list = self.get_case_list()
        for line in run_list:
            if pre in dict(line).values():
                return line
        return None


if __name__ == '__main__':
    pass