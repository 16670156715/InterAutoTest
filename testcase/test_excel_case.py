from config.Conf import ConfigYml
from config import Conf
import os
from common.EXcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
import json
import pytest
from common import Base
from utils.AssertUtil import AssertUtil
import allure


# 1、初始化信息
case_file = os.path.join(Conf.get_data_path(), ConfigYml().get_excel_file())    # 初始化测试用例文件
sheet_name = ConfigYml().get_excel_sheet()  # 初始化测试用例sheet名称
# 获取运行测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_data()
log = my_log()  # 日志
data_key = ExcelConfig.DataConfig   # 初始化DataConfig


# 2、测试用例方法，参数化运行
class TestExcel:
    def run_api(self, url, method, url_params, reference, params=None, header=None, cookie=None):
        """
        发送请求api
        :param url:
        :param method:
        :param params:
        :param header:
        :param cookie:
        :return:
        """
        request = Request()
        # params 转义json
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        if str(method).lower() == "get" and str(reference).lower() == "b":
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "get" and str(reference).lower() == "u":
            res = request.get(url_params, headers=header, cookies=cookie)
        elif str(method).lower() == "post" and str(reference).lower() == "b":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post" and str(reference).lower() == "u":
            res = request.post(url_params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method： %s" % method)
        return res

    def run_pre(self, pre_case):
        # 初始化数据
        pass
        url = ConfigYml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        reference = pre_case[data_key.reference]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]
        # 判断headers和cookie是否存在，如果存在json转义，如果不存在无需转义
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        url_params = Base.joint_url(pre_case[data_key.params], pre_case[data_key.url])
        res = self.run_api(url, method, url_params, reference, params, header)
        print("前置用例执行：%s" % res)
        return res

    def get_correlation(self, headers, cookies, pre_res):
        """
        关联
        :param headers:
        :param cookies:
        :param pre_res:
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res["body"]["data"][headers_para[0]]
            headers = Base.res_sub(headers, headers_data)   # 结果替换
        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]
            cookies = Base.res_sub(cookies, cookies_data)   # 结果替换
        return headers, cookies

    @pytest.mark.parametrize("case", run_list)
    def test_run(self, case):
        # 初始化信息，url.data 等数据
        url = ConfigYml().get_conf_url() + case[data_key.url]
        print(url)
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        reference = case[data_key.reference]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verity = case[data_key.db_verity]

        # 验证前置条件
        if pre_exec:
            pass
            # 找到执行用例，前置测试用例
            pre_case = data_init.get_case_pre(pre_exec)
            # print("前置条件信息为：%s" % pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)
        # 判断headers和cookie是否存在，如果存在json转义，如果不存在无需转义
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        url_params = Base.joint_url(case[data_key.params], case[data_key.url])
        res = self.run_api(url, method, url_params, reference, params, header, cookie)
        print("测试用例执行：%s" % res)

        # allure
        allure.dynamic.feature(sheet_name)  # sheet名称   feature 一级标签
        allure.dynamic.story(case_model)    # 模块    story 二级标签
        allure.dynamic.title(case_id+case_name)     # 用例ID+接口名称 title
        # 请求URL 请求类型 期望结果 实际结果描述
        desc = "<font color='red'>请求URL: </font> {}<Br/>" \
               "<font color='red'>请求类型: </font>{}<Br/>" \
               "<font color='red'>期望结果: </font>{}<Br/>" \
               "<font color='red'>实际结果: </font>{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # 断言验证
        assert_util = AssertUtil()
        assert_util.assert_code(int(res["code"]), int(code))        # 验证状态码
        assert_util.assert_in_body(str(res["body"]), str(expect_result))    # 验证返回结果内容
        if len(db_verity) > 0:  # 数据库结果断言
            Base.assert_db("db_1", res["body"], db_verity)


if __name__ == '__main__':
    # pass
    report_path = Conf.get_report_path() + os.sep + "result"
    report_html_path = Conf.get_report_path() + os.sep + "html"
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_path])
    Base.allure_report(report_path, report_html_path)
    Base.send_mail(title="接口测试报告结果", content=report_html_path)
