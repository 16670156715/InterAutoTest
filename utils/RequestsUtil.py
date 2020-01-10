import requests


class Request:
    def requests_api(self, url, data=None, json=None, headers=None, cookies=None, method="get"):
        # 根据参数来验证方法get、post，方法请求
        if method == "get":
            # get 请求
            r = requests.get(url, data=data, json=json, headers=headers, cookies=cookies)
        elif method == "post":
            # post 请求
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
