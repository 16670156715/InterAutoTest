import json
import re
import subprocess

from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
from utils.MysqlUtil import Mysql
from config.Conf import ConfigYml
from utils.EmailUtil import SendEmail

p_data = '\${(.*)}\$'
log = my_log()


# 定义init_db
def init_db(db_alias):
    """
    初始化配置文件，并初始化mysql对象
    :param db_alias:
    :return:
    """
    db_info = ConfigYml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = int(db_info["db_port"])
    conn = Mysql(host, user, password, db_name, charset, port)
    return conn


def assert_db(db_name, result, db_verity):
    """
    数据库结果断言封装
    :param db_name:
    :param result:
    :param db_verity:
    :return:
    """
    assert_util = AssertUtil()
    sql = init_db(db_name)
    # 查询sql，Excel定义好的
    db_res = sql.fetchone(db_verity)
    # log.debug("数据库查询结果：{}".format(str(db_res)))
    # 获取数据库结果的key
    verify_list = list(dict(db_res).keys())
    # 根据key获取数据库结果，接口结果
    for line in verify_list:
        if line is None:
            # print(type(line))
            res_line = result[line]
            # print(res_line)
            res_db_line = dict(db_res)[line]
            # 验证
            assert_util.assert_in_body(res_db_line, res_line)


def json_parse(data):
    """
    格式化字符，转换json
    :param data:
    :return:
    """
    return json.loads(data) if data else data


def res_find(data, pattern_data=p_data):
    """
    查询
    :param data:
    :param pattern_data:
    :return:
    """
    # pattern = re.compile('\${(.*)}\$')
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res


def res_sub(data, replace, pattern_data=p_data):
    """
    替换
    :param data:
    :param replace:
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data, replace, data)
    return re_res


def params_find(headers, cookies):
    """
    验证请求中是否有${}$需求结果关联
    :param headers:
    :param cookies:
    :return:
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    return headers, cookies


def allure_report(report_path, report_html):
    """
    生成allure报告
    :param report_path:
    :param report_html:
    :return:
    """
    # 执行命令 allure generate
    allure_cmd = "allure generate %s -o %s --clean" % (report_path, report_html)
    print(allure_cmd)
    # subprocess.call
    log.info("报告地址")
    try:
        subprocess.call(allure_cmd, shell=True)
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise


def joint_url(params, url):
    """
    将url和请求参数拼接
    :param params:
    :param url:
    :return:
    """
    params_data = json.loads(params)  # 将字符串转换为字典
    url_params = ConfigYml().get_conf_url() + url + "?"
    for key in params_data:  # 把请求参数拼接到url地址中
        url_params = url_params + key + "=" + params_data[key] + "&"
    url_params = url_params[:-1]  # 删除最后一个 &
    return url_params


def send_mail(report_html_path="",content="",title="测试"):
    """
    发送邮件
    :param report_html_path:
    :param content:
    :param title:
    :return:
    """
    email_info = ConfigYml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(
        smtp_addr=smtp_addr,
        username=username,
        password=password,
        recv=recv,
        title=title,
        content=content,
        file=report_html_path)
    email.send_mail()


if __name__ == '__main__':
    # init_db("db_1")
    # print(res_find('{"Authorization": "${token}$"}'))
    # print(res_sub('{"Authorization": "${token}$"}', "123"))
    print(allure_report("../report/result", "../report/html"))
