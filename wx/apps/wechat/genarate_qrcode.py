#!/usr/bin/python3 
# -*-coding:utf-8-*- 
# @Author: zhu shiqing
# @Time: 2018年05月10日02时07分 
# 说明: 
# 总结:
import time
import urllib2
import json
from flask import Flask, request

WECHAT_ID = "wx18c8e575575c3cdd"
WECHAT_SECRET = "1c2607fcb30cdc3e964d137d3c6117cc"


class AccessToken(object):
    '''提供微信的接口调用凭据'''
    # 数据 属性
    __access_token = {
        "token": "",  # 真实的token数据
        "update_time": time.time(),  # 更新时间
        "expires_in": 7200,  # token的有效期
    }

    # 函数 方法
    @classmethod
    def get_access_token(cls):
        # 如果保存的access_token超过了有效期，从新从微信服务器获取，并保存，再返回
        if not cls.__access_token["token"] or (time.time() - cls.__access_token["update_time"]) > (
                cls.__access_token["expires_in"] - 600):

            # 重新调用微信接口，从新获取
            url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
            WECHAT_ID, WECHAT_SECRET)

            response = urllib2.urlopen(url)
            resp_json = response.read()
            resp_dict = json.loads(resp_json)
            if "errcode" in resp_dict:
                # 微信处理失败
                raise Exception("get access token failed")

            else:
                cls.__access_token["token"] = resp_dict.get("access_token")
                cls.__access_token["expires_in"] = resp_dict.get("expires_in")
                cls.__access_token["update_time"] = time.time()
                return cls.__access_token["token"]

        else:
            # 如果没有过期，则直接返回保存的token
            return cls.__access_token["token"]


app = Flask(__name__)


@app.route("/zsq/get_qrcode")
def get_qrcode():
    scene_id = request.args.get("id")
    access_token = AccessToken.get_access_token()
    # 让微信生成临时二维码
    url = " https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token

    req_data = {
        "expire_seconds": 604800,
        "action_name": "QR_SCENE",
        "action_info": {"scene": {"scene_id": scene_id}}

    }
    response = urllib2.urlopen(url, data=json.dumps(req_data))
    reqs_json = response.read()
    reqs_dict = json.loads(reqs_json)

    if "errcode" in reqs_dict:
        return "generate grcode falie"

    else:
        ticket = reqs_dict.get("ticket")
        # 指使微信生成二微码成功'
        return '<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"><br/><p>%s</p>' % (ticket, reqs_dict.get("url"))


if __name__ == '__main__':
    app.run(debug=True, port=5001)