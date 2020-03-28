import os
import xlrd


# 目的：参数化，pytest list
# 自定义异常
class SheetTypeError:
    pass


class ExcelReader:
    """
    验证文件是否存在，存在就读取，不存在报错
    """
    def __init__(self, excel_file, sheet_by):
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.sheet_by = sheet_by
            self._data = list()
        else:
            raise FileNotFoundError("文件不存在")

    def data(self):
        """
        读取sheet方式，名称、索引
        :return:
        """
        if not self._data:    # 存在不读取，不存在读取
            workbook = xlrd.open_workbook(self.excel_file)
            if type(self.sheet_by) not in [str, int]:
                raise SheetTypeError("请输入Int or Str")
            elif type(self.sheet_by) == int:
                sheet = workbook.sheet_by_index(self.sheet_by)
            elif type(self.sheet_by) == str:
                sheet = workbook.sheet_by_name(self.sheet_by)
            # 读取sheet内容，返回数据格式[{"a":"a1","b":"b1"},{"a":"a2","b":"b2"}]
            title = sheet.row_values(0)     # 获取首行的信息
            # 遍历测试行，与首行组成dict，放在list中，过滤首行，从1开始
            for col in range(1, sheet.nrows):
                col_value = sheet.row_values(col)
                self._data.append(dict(zip(title, col_value)))  # 与首行组成字典，放入list
        return self._data   # 结果返回


if __name__ == '__main__':
    reade = ExcelReader("../data/testdata.csv", "api")
    print(reade.data())
