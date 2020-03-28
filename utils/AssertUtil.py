from utils.LogUtil import my_log
import json


class AssertUtil:
    # 初始化数据，日志
    def __init__(self):
        self.log = my_log("AssertUtil")

    # code相等
    def assert_code(self, code, expected_code):
        """
        验证返回的状态码与实际的状态码是否相等
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("code error,code is %s, expected_code is %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """
        验证返回结果内容相等
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("body error,body is %s, expected_body is %s" % (body, expected_body))
            raise

    def assert_in_body(self, body, expected_body):
        """
        验证返回的body中是否包含期望的body
        :param body:
        :param expected_body:
        :return:
        """
        try:
            # body = json.dumps(body)
            assert expected_body in body
            return True
        except:
            print("实际的body为 %s" % body)
            self.log.error("不包含或者body是错误, body is %s, expected_body is %s" % (body, expected_body))

            raise
