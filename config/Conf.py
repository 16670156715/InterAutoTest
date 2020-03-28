import os
from utils.YamlUtil import YamlReader
#
current = os.path.abspath(__file__)
# print(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)
# 定义config目录路径
_config_path = BASE_DIR + os.sep + "config"
# 定义data目录路径
_data_path = BASE_DIR + os.sep + "data"
# print(_data_path)
# 定义conf.yml文件路径
_config_file = _config_path + os.sep + "conf.yml"
# 定义db_conf.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
# 定义文件路径
_log_path = BASE_DIR + os.sep + "logs"
# 定义report目录路径
_report_path = BASE_DIR + os.sep + "report"
print(_report_path)


def get_report_path():
    """
    获取report绝对路径
    :return:
    """
    return _report_path


def get_db_config_file():
    """
    获取数据库参数
    :return:
    """
    return _db_config_file


def get_config_path():
    """
    获取配置文件路径
    :return:
    """
    return _config_path


def get_data_path():
    """
    获取测试数据文件路径
    :return:
    """
    return _data_path


def get_config_file():
    """
    获取配置文件
    :return:
    """
    return _config_file


def get_log_path():
    """
    获取Log文件路径
    :return:
    """
    return _log_path


class ConfigYml:
    # 初始化yml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    # 定义方法获取需要信息
    def get_conf_url(self):
        """
        获取URL地址
        :return:
        """
        return self.config["BASE"]["test"]["url"]

    def get_excel_file(self):
        """
        获取测试用例名称
        :return:
        """
        return self.config["BASE"]["test"]["case_file"]

    def get_excel_sheet(self):
        """
        获取测试用例sheet名称
        :return:
        """
        return self.config["BASE"]["test"]["case_sheet"]

    def get_conf_log(self):
        """
        获取日志级别
        :return:
        """
        return self.config["BASE"]["log_level"]

    def get_conf_log_extension(self):
        """
        获取日志扩展名
        :return:
        """
        return self.config["BASE"]["log_extension"]

    def get_db_conf_info(self, db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        :return:
        """
        return self.config["email"]


if __name__ == '__main__':
    conf_read = ConfigYml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_log_extension())
    # print(conf_read.get_db_conf_info("db_1"))
    # print(conf_read.get_excel_file())
    # print(conf_read.get_excel_sheet())
    print(conf_read.get_email_info())

