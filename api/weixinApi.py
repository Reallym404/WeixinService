import web
from spider.lifeService import LifeSpider
import config
import sys
import os

urls = (
    '/weixin','weixin',
    '/mobile', 'mobile',
    '/kuaidi', 'kuaidi',
    '/index','pic'
)

class pic():
    def GET(self):
        inputs = web.input()
        name = inputs.get('name')
        path = r'F:\Code\PythonProj\WeixinService\mzitu' + os.path.sep +name +'.jpg'
        return open(path,'rb')

class weixin():
    def GET(self):
        return 'index'


# 手机号码归属地查询
class mobile():
    lifeService = LifeSpider()
    def GET(self):
        inputs = web.input()
        mobile_num = inputs.get('mobile')
        #print(mobile_num)
        result = self.lifeService.mobile(mobile_num)
        #return json.dumps(result)
        return result

# 快递单号 物流信息
class kuaidi():
    lifeService = LifeSpider()
    def GET(self):
        inputs = web.input()
        kuaidi_num = inputs.get('no')
        # print(mobile_num)
        result = self.lifeService.kuaidi(kuaidi_num)
        #return json.dumps(result)
        return result

if __name__ == '__main__':
    #sys.argv.append('0.0.0.0:%s' % config.PORT)
    app = web.application(urls,globals())
    app.run()