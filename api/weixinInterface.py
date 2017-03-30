import web
from lxml import etree
import xml.etree.ElementTree as ET
import hashlib
import lxml
import time
import os
import json
import config
import sys
from spider.lifeService import LifeSpider
from db.DbHelper import dbHelper



urls = (
    '/weixin','Weixin',
    '/index', 'index',
)



if __name__ == '__main__':
    sys.argv.append('0.0.0.0:%s' % config.WEIXIN_PORT)
    app = web.application(urls,globals())
    app.run()


class index():
    def GET(self):
        inputs = web.input()
        name = inputs.get('name')
        path = r'D:\mzitu' + os.path.sep + name
        return open(path, 'rb')

class Weixin:

    def __init__(self):
        """
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)
        """
        self.life = LifeSpider()

    def GET(self):
        # 获取输入参数
        data = web.input()
        signature = data.get('signature')
        timestamp = data.get('timestamp')
        nonce = data.get('nonce')
        echostr = data.get('echostr')
        print(signature,timestamp,nonce,echostr)
        token = config.WEIXIN_TOKEN  # token
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        #map(sha1.update, list)
        # hashcode = sha1.hexdigest()

        # sha1加密算法
        hashcodestr = ''.join(list)
        sha1.update(hashcodestr.encode('utf-8'))
        hashcode = sha1.hexdigest()

        print(signature, timestamp, nonce, echostr,hashcode)
        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr

    def POST(self):
        '''
        遇到问题：微信发英文消息时没有问题；当发中文消息时出现无法解析问题，可能是文件编码，文件编码设为utf-8 ，或者在pyCharm设置里
            设置FileEncode 为 utf-8
         '''
        str_xml = web.data()   # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text

        # 关注自动回复
        if msgType == 'event':
            try:
                Event = xml.find('Event').text
                if Event == 'subscribe':
                    # 关注自动回复
                    reply_content = u'欢迎关注我的公众号\n'+config.DEFAULT_REPLY_TEXT
                    return self.reply_text(fromUser, toUser, int(time.time()), reply_content)
            except:
                pass
        # 文本消息
        elif msgType == 'text':
            content = xml.find("Content").text  # 获得用户所输入的内容
            if u"使用" in content:
                return self.reply_text(fromUser, toUser, int(time.time()), config.DEFAULT_REPLY_TEXT)
            elif content[0:2] == u"手机":
                mobile_num = content[2:]
                mobile_text = self.life.mobile(mobile_num)
                return self.reply_text(fromUser, toUser, int(time.time()), mobile_text+" ")
            elif content[0:2] == u"快递":
                kuaidi_num = content[2:]
                kuaidi_text = self.life.kuaidi(kuaidi_num)
                return self.reply_text(fromUser, toUser, int(time.time()), kuaidi_text + " ")
            elif u'天气' == content[0:2]:
                addr = content[2:]
                weather_text = self.life.weather1(addr)
                return self.reply_text(fromUser, toUser, int(time.time()), weather_text + " ")
            elif u'天气' == content[-2:]:
                addr = content[:-2]
                weather_text = self.life.weather1(addr)
                return self.reply_text(fromUser, toUser, int(time.time()), weather_text + " ")
            elif content[0:2] == u"建议":
                info = content[2:]
                if len(info) < 5:
                    return self.reply_text(fromUser, toUser, int(time.time()), config.SUGGEST_TIP)
                else:
                    db = dbHelper()
                    db.suggest(info)
                    return self.reply_text(fromUser, toUser, int(time.time()), config.SUGGEST_BACK)
            elif u"段子" in content:
                duanzi_text = self.life.duanzi()
                return self.reply_text(fromUser, toUser, int(time.time()), duanzi_text)
            elif u"邮编" == content[-2:]:
                area = content[:-2]
                youbian_text = self.life.youbian(area)
                return self.reply_text(fromUser, toUser, int(time.time()), youbian_text)
            elif u"叶铭" == content or u'小叶子' == content:
                return self.reply_text(fromUser, toUser, int(time.time()),config.DEFAULT_REPLY_TEXT1)
            elif u"美女" == content or u'妹纸' == content or u'妹子' == content :
                text = 'http://ymboy.xyz/index?name=mzitu1'+ '.jpg'
                return self.reply_text(fromUser, toUser, int(time.time()),text)
            elif u'运势' == content[-2:]:
                astro = content[:-2]
                astro_text = self.life.constellation(astro)
                return self.reply_text(fromUser, toUser, int(time.time()), astro_text + " ")
            else:
                return self.reply_text(fromUser, toUser, int(time.time()), config.DEFAULT_REPLY_TEXT)
        # 图片消息
        elif msgType == 'image':
            pass
        else:
            pass

    def check_none(self,check_text):
        return len(check_text)

    """回复文本消息模板"""
    def reply_text(self, FromUserName, ToUserName, CreateTime, Content):
        textTpl = """<xml> <ToUserName><![CDATA[%s]]></ToUserName> <FromUserName><![CDATA[%s]]></FromUserName> <CreateTime>%s</CreateTime> <MsgType><![CDATA[%s]]></MsgType> <Content><![CDATA[%s]]></Content></xml>"""
        out = textTpl % (FromUserName, ToUserName, CreateTime, 'text', Content)
        return out