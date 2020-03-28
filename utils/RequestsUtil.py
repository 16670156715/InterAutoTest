import requests
from utils.LogUtil import my_log


class Request:
    def __init__(self):
        self.log = my_log("Requests")

    def requests_api(self, url, data=None, json=None, headers=None, cookies=None, method="get"):
        # 根据参数来验证方法get、post，方法请求
        if method == "get":
            # get 请求
            self.log.debug("发送get请求")
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "post":
            # post 请求
            self.log.debug("发送post请求")
            r = requests.post(url, data=data, json=json, headers=headers, cookies=cookies)
        # 获取结果内容
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        # 字典返回
        return res

    # 重构get/post方法
    def get(self, url, **kwargs):
        return self.requests_api(url, method="get", **kwargs)

    # 重构get/post方法
    def post(self, url, **kwargs):
        return self.requests_api(url, method="post", **kwargs)


if __name__ == '__main__':
    request = Request()
    print(request.post(
        "https://api.create-chain.net/ccmapi/login?username=15573235704&password=20216565&deviceType=phone&type=1"))
