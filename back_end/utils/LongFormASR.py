import base64
import hashlib
import hmac
import json
import os
import time
import urllib

import requests

from .app_config import lfasr_host, lfasr_upload, lfasr_get_result


class ConverterApi(object):
    def __init__(self, appid, secret_key):
        self.appid = appid
        self.secret_key = secret_key
        self.ts = str(int(time.time()))
        self.signa = self.get_signa()

    def get_signa(self):
        appid = self.appid
        secret_key = self.secret_key
        m2 = hashlib.md5()
        m2.update((appid + self.ts).encode('utf-8'))
        md5 = m2.hexdigest()
        md5 = bytes(md5, encoding='utf-8')
        # 以secret_key为key, 上面的md5为msg， 使用hashlib.sha1加密结果为signa
        signa = hmac.new(secret_key.encode('utf-8'), md5, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')
        return signa

    def upload(self, upload_file_path):
        print("上传部分：")
        file_len = os.path.getsize(upload_file_path)
        file_name = os.path.basename(upload_file_path)

        param_dict = {}
        param_dict["appId"] = self.appid
        param_dict["signa"] = self.signa
        param_dict["ts"] = self.ts
        param_dict["fileSize"] = file_len
        param_dict["fileName"] = file_name
        param_dict["duration"] = "200"
        #TODO 部署后开启回调
        param_dict["callbackUrl"] = "http://101.37.80.29:5000/callback"
        print("upload参数：", param_dict)
        data = open(upload_file_path, 'rb').read(file_len)

        response = requests.post(url=lfasr_host + lfasr_upload + "?" + urllib.parse.urlencode(param_dict),
                                 headers={"Content-type": "application/json"}, data=data)
        result = json.loads(response.text)
        return result

    def query_result(self, orderId):
        params = {}
        params["appId"] = self.appid
        params["signa"] = self.signa
        params["ts"] = self.ts
        params["orderId"] = orderId
        params["resultType"] = "transfer"
        response = requests.post(
            url=lfasr_host + lfasr_get_result + "?" + urllib.parse.urlencode(params),
            headers={"Content-type": "application/json"})
        return response.text

    def get_result(self):
        uploadresp = self.upload()
        orderId = uploadresp['content']['orderId']
        param_dict = {}
        param_dict['appId'] = self.appid
        param_dict['signa'] = self.signa
        param_dict['ts'] = self.ts
        param_dict['orderId'] = orderId
        param_dict['resultType'] = "transfer,predict"
        print("")
        print("查询部分：")
        print("get result参数：", param_dict)
        status = 3
        # 建议使用回调的方式查询结果，查询接口有请求频率限制
        while status == 3:
            response = requests.post(
                url=lfasr_host + lfasr_get_result + "?" + urllib.parse.urlencode(param_dict),
                headers={"Content-type": "application/json"})
            # print("get_result_url:",response.request.url)
            result = json.loads(response.text)
            print(result)
            status = result['content']['orderInfo']['status']
            print("status=", status)
            if status == 4:
                break
            time.sleep(10)
        print("get_result resp:", result)
        return result

    def converter(self):
        #TODO
        pass