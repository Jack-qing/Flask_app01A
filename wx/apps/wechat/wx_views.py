#!/usr/bin/python3 
# -*-coding:utf-8-*- 
# @Author: zhu shiqing
# @Time: 2018年05月09日19时18分 
# 说明: 
# 总结:

from flask import Flask, request, abort
import hashlib
import xmltodict
import time
app = Flask(__name__)

WECHAT_TOKEN = "zhushiqing"


@app.route('/zsq/wechat', methods=["GET", "POST"])
def wechat():
    u'''对接微信服务器'''
    # 获取参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    echostr = request.args.get("echostr")

    # 进行参数计算
    # 1 进行排序
    li = [WECHAT_TOKEN, timestamp, nonce]
    li.sort()

    # 2 拼接成字符串
    tmp_str = "".join(li)
    print("1111")

    # 3 进行sha1加密  hexdigest拿到加密的返回值
    sign = hashlib.sha1(tmp_str).hexdigest()

    if signature != sign:
        # 不是微信发送过来的请求，拒绝
        abort(403)

    else:
        # 如果是GET请求，表示初始化请求
        if request.method == "GET":
            # 如果与微信传过来的参数相匹配，则返回echostr
            return echostr
        else:
            # post 请求表示用户发送转发消息
            # 接收消息
            rep_xml = request.data
            xml_dict = xmltodict.parse(rep_xml)
            xml_dict = xml_dict["xml"]
            # 封装响应消息
            # MsgType = 转为txt
            msg_type = xml_dict.get("MsgType")
            if msg_type == "text":
                # 表不文字类型
                # 构建返回的字典数据
                resp_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": xml_dict.get("Content")
                }
            elif msg_type == "voice":
                # 语音类型
                resp_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": xml_dict.get("Recognition"),
                }

            else:
                resp_dict = {
                    "ToUserName": xml_dict.get("FromUserName"),
                    "FromUserName": xml_dict.get("ToUserName"),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": "i love u"
                }

            resp_dict = {"xml":resp_dict}
            return xmltodict.unparse(resp_dict)




if __name__ == '__main__':
    app.run(port=5001, debug=True)
