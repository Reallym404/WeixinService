from spider.lifeService import LifeSpider
from weixin.WeixinUtil import WeixinApi
import os
import re

if __name__ == '__main__':
    life = LifeSpider()
    #print(life.mobile(1))
    #print(life.kuaidi(430226383158))
    #print(len(life.duanzi()))
    #print(life.duanzi())
    #print(life.weather('龙南'))
    #print(life.weather1('龙南'))
    #print(life.youbian('龙南'))

    #weixinapi = WeixinApi()
    #print(weixinapi.get_token())
    # print(weixinapi.get_media_count())


    #print(os.path.dirname(__file__))

    print(life.constellation('双鱼'))
