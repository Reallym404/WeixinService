import requests
import config
from lxml import etree
import re
import random
import json

# http://m.ip138.com/
# iP138 网站服务接口

class LifeSpider():
    mobile_url = 'http://m.ip138.com/mobile.asp'
    kuaidi_url = 'http://m.ip138.com/kuaidi/search.asp'
    #duanzi_url = 'http://www.qiushibaike.com/'
    #duanzi_hot_url = 'http://www.qiushibaike.com/hot/'
    #duanzi_url = 'http://duanziwang.com/category/duanzi'
    duanzi_url ='http://www.toutiao.com/api/article/feed/'
    weather_url = 'http://qq.ip138.com/tianqi/tianqi.asp'
    weather_url1 = 'http://wthrcdn.etouch.cn/weather_mini'
    youbian_url = 'http://m.ip138.com/youbian/youbian.asp'
    astro_url = 'http://dps.3g.qq.com/dps/api'
    ## http://m.ip138.com/mobile.asp?mobile=********

    ## 查询手机号归属地
    def mobile(self,mobile_num):

        result = ''
        headers = config.get_header()
        headers['Referer'] = 'http://m.ip138.com/mobile.html'

        format_data={
            'mobile':mobile_num
        }
        try:
            res = requests.get(url=self.mobile_url,params=format_data,headers=headers, timeout=config.TIMEOUT)
            #print(res.text)
        except requests.exceptions.Timeout:
            print('Request timed out. (timeout=%s)'%config.TIMEOUT)
            return 'Request timed out,please try again!'
        if res.status_code == 200:
            soup = etree.HTML(res.content)
            selector = soup.xpath('//table[@class="table"]/tr')
            er = soup.xpath('//table[@class="table"]/tr/td[@colspan="2"]/text()')
            if len(er):
                result = er[0]
                #return result
            else:
                for table in selector:
                    td_key = table.xpath('./td/text()')[0]
                    td_var = table.xpath('./td/span/text()')[0]
                    #result[td_key] = td_var
                    result = result + td_key + ":" + td_var + '\n'
                #print(result)

        else:
            return '查询失败,请重试!'
        return result

    ## 快递单号 物流信息
    def kuaidi(self,kuaidi_no):
        result = ''
        headers = config.get_header()
        headers['Referer'] = 'http://m.ip138.com/kuaidi/search.asp'

        format_data = {
            'no':kuaidi_no
        }
        try:
            res = requests.post(url=self.kuaidi_url,data=format_data,headers=headers, timeout=config.TIMEOUT)
            res.encoding = 'utf-8'
            #print(res.text)
        except requests.exceptions.Timeout:
            print('Request timed out. (timeout=%s)'%config.TIMEOUT)
            return 'Request timed out,please try again!'
        soup = etree.HTML(res.content)
        selector = soup.xpath('//ul[@class="query-hd"]/li')
        title = soup.xpath('//ul[@class="query-hd"]/li[@class="title"]')
        comany = title[0].xpath('./span[@class="comany"]/text()')
        #print(comany)
        if len(comany) == 0:
            result = selector[-1].xpath('./text()')[0]
            #return result
        else:
            comany = title[0].xpath('./span/text()')[0]
            status = title[0].xpath('./span/text()')[1]
            #print(comany,status)
            result = result + comany +","+status + '\n'
            for li in selector[1:-1]:
                time = li.xpath('./div[@class="time"]/text()')[0]
                detail = li.xpath('./div[@class="detail"]/text()')[0]
                result = result + time + " - " +detail + '\n'
            #print(result)
        return result

    # 天气
    def weather(self,addr):
        result = ''
        headers = config.get_header()
        format_data = {
            'addr': addr
        }
        res = requests.get(url=self.weather_url, params=format_data, headers=headers)
        #print(res.text)
        soup = etree.HTML(res.content)
        selector = soup.xpath('//ul[@class="query-hd"]')
        #print(selector)
        if len(selector) == 0:
            result = u'没找到这个城市的天气预报!'
        else:
            ul = soup.xpath('//ul[@class="query-hd"]/li')
            date = ul[0].xpath('./div[@class="date"]/text()')[0]
            phrase = ul[0].xpath('./div[@class="phrase"]/text()')[0]
            temperature = ul[0].xpath('./div[@class="temperature"]/text()')[0]
            result = result + date + u'今天' + " " + phrase +' '+ temperature + '\n'
            for li in ul[1:]:
                date = li.xpath('./div[@class="date"]/text()')[0]
                phrase = li.xpath('./div[@class="phrase"]/text()')[0]
                temperature = li.xpath('./div[@class="temperature"]/text()')[0]
                result = result + date + " " + phrase + ' ' + temperature + '\n'
        return result

    # 天气1
    def weather1(self, city):
        result = ''
        headers = config.get_header()
        format_data = {
            'city': city
        }
        res = requests.get(url=self.weather_url1, params=format_data, headers=headers)
        status = res.json().get('status')
        if int(status) == 1000:
            data = res.json().get('data')
            yesterday_data = data.get('yesterday')
            yesterday_date = yesterday_data.get('date')
            yesterday_type = yesterday_data.get('type')
            yesterday_high = yesterday_data.get('high')
            yesterday_high = str(yesterday_high).replace(" ",'')
            yesterday_low = yesterday_data.get('low')
            yesterday_low = str(yesterday_low).replace(" ", '')
            yesterday_fl = yesterday_data.get('fl')
            yesterday_fx = yesterday_data.get('fx')
            yesterday = '{0}  {1}  {2}/{3} {4} {5}'.format(yesterday_date,yesterday_type,yesterday_high,yesterday_low,yesterday_fx,yesterday_fl)
            result = result + yesterday + '\n'

            forecast = data.get('forecast')
            today_data = forecast[0]
            today_fx = today_data.get('fengxiang')
            today_fl = today_data.get('fengli')
            today_high = today_data.get('high')
            today_type = today_data.get('type')
            today_low = today_data.get('low')
            today_date = today_data.get('date')
            today_date = u'今天'+str(today_date).split(u'日')[1]
            today = '{0}  {1}  {2}/{3} {4} {5}'.format(today_date, today_type, today_high, today_low, today_fx, today_fl)
            result = result + today + '\n'

            for f in forecast[1:]:
                fx = f.get('fengxiang')
                fl = f.get('fengli')
                high = f.get('high')
                type = f.get('type')
                low = f.get('low')
                date = f.get('date')
                forecast_data = '{0}  {1}  {2}/{3} {4} {5}'.format(date,type,high,low,fx,fl)
                result = result + forecast_data + '\n'
        else:
            result = u'没找到这个城市的天气预报!'
        return result

    # 热门段子
    def duanzi(self):
        headers = config.get_header()
        headers['Referer'] = 'http://www.toutiao.com/essay_joke/'
        param = {
            'category': 'essay_joke',
            'utm_source': 'toutiao',
            'widen': '1',
            'max_behot_time': '0',
            'max_behot_time_tmp':' 0',
            'tadrequire ':'true',
            'as':'A115B81C539BB39',
            'cp':'58C31BCB03C90E1'
        }
        res = requests.get(url=self.duanzi_url,headers=headers,params=param)
        #print(res.text)
        result = res.json()
        data = result['data']
        text_list = []
        for o in data:
            group = o['group']
            text = group['text']
            text_list.append(text)
        text = random.choice(text_list)
        return text

    #输入地名查询邮编
    def youbian(self,area):
        headers = config.get_header()
        format_data = {
            'area':area,
            'action':'area2zip'
        }
        res = requests.get(url=self.youbian_url, params=format_data, headers=headers)
        #print(res.text)
        soup = etree.HTML(res.content)
        result = soup.xpath('//div[@class="container"]/div[@class="module"]/p[@class="query-hd"]/text()')[0]
        return str(result)


    # 星座运势
    """
    白羊座:0 金牛座:1 双子座:2 巨蟹座:3 狮子座:4 处女座:5
    天秤座:6 天蝎座:7 射手座:8 摩羯座:9 水瓶座:10 双鱼座:11
    """
    def constellation(self,astro):
        result = ''
        current_astro = '0'
        if u'白羊座' in astro or u'白羊' in astro:
            current_astro = '0'
        elif u'金牛座' in astro or u'金牛' in astro:
            current_astro = '1'
        elif u'双子座' in astro or u'双子' in astro:
            current_astro = '2'
        elif u'巨蟹座' in astro or u'巨蟹' in astro:
            current_astro = '3'
        elif u'狮子座' in astro or u'狮子' in astro:
            current_astro = '4'
        elif u'处女座' in astro or u'处女' in astro:
            current_astro = '5'
        elif u'天秤座' in astro or u'天秤' in astro:
            current_astro = '6'
        elif u'天蝎座' in astro or u'天蝎' in astro:
            current_astro = '7'
        elif u'射手座' in astro or u'射手' in astro:
            current_astro = '8'
        elif u'摩羯座' in astro or u'摩羯' in astro:
            current_astro = '9'
        elif u'水瓶座' in astro or u'水瓶' in astro:
            current_astro = '10'
        elif u'双鱼座' in astro or u'双鱼' in astro:
            current_astro = '11'
        else:
            current_astro = '12'

        if current_astro == '12':
            result = u'请输入要查询的星座名称(如：天秤座运势)!'
            return result
        else:
            detail = self.astro_detail(current_astro)
            fortune_week = self.astro_fortune_week(current_astro)
            fortune_day = self.astro_fortune_day(current_astro)
            result = result + detail + fortune_day + fortune_week
        return result

    # 星座详情
    def astro_detail(self,astro):
        #http://dps.3g.qq.com/dps/api?module=astro&action=get_astro_detail&type=info&choosed_astro=11
        headers = config.get_header()
        param = {
            'module': 'astro',
            'action': 'get_astro_detail',
            'type': 'info',
            'choosed_astro': astro
        }
        res = requests.get(url=self.astro_url,headers=headers,params=param)
        data_json = res.json()
        data = data_json.get('data')
        astro_date = data.get('astro_date')
        astro_name = data.get('astro_name')
        info_status = data.get('info_status')
        title = astro_name+"("+astro_date+")"
        text = ''
        for k in info_status.keys():
            var = info_status[k]
            text = text + k + ":" + var +"\n"
        result = title + "\n" + text +'\n'
        return result

    #今日运势
    def astro_fortune_day(self,astro):

        # http://dps.3g.qq.com/dps/api?module=astro&action=go108_astro_fortune&range=day&current_astro=11
        headers = config.get_header()
        param = {
            'module': 'astro',
            'action': 'go108_astro_fortune',
            'range': 'day',
            'current_astro': astro
        }
        result = u"今日运势: \n"
        res = requests.get(url=self.astro_url, headers=headers, params=param)
        data_json = res.json()
        data = data_json.get('data')
        lucky_status = data.get('lucky_status')
        other_status = data.get('other_status')
        overview = data.get('overview')

        lucky_text = '运势(5):'
        for k in lucky_status.keys():
            var = lucky_status[k]
            lucky_text = lucky_text + k + "-" + str(var) + "  "

        lucky_text = lucky_text + '\n'

        other_text = ''
        for k in other_status.keys():
            var = other_status[k]
            other_text = other_text + k + ":" + var + "\n"

        overview_text = ''
        for k in overview.keys():
            var = overview[k]
            overview_text = overview_text + k + ":" + var + "\n"

        result = result + lucky_text + other_text + overview_text + "\n"
        return result

    #星座一周运势
    def astro_fortune_week(self,astro):

        # http://dps.3g.qq.com/dps/api?module=astro&action=go108_astro_fortune&range=week&current_astro=0
        headers = config.get_header()
        param = {
            'module': 'astro',
            'action': 'go108_astro_fortune',
            'range': 'week',
            'current_astro': astro
        }
        result = u"本周运势: \n"
        res = requests.get(url=self.astro_url, headers=headers, params=param)
        data_json = res.json()
        data = data_json.get('data')
        lucky_status = data.get('lucky_status')
        other_status = data.get('other_status')
        overview = data.get('overview')

        lucky_text = '运势(5):'
        for k in lucky_status.keys():
            var = lucky_status[k]
            lucky_text = lucky_text + k + "-" + str(var) + "  "

        lucky_text = lucky_text + '\n'

        other_text = ''
        for k in other_status.keys():
            var = other_status[k]
            other_text = other_text + k + ":" + var + "\n"

        overview_text = ''
        for k in overview.keys():
            var = overview[k]
            overview_text = overview_text + k + ":" + var + "\n"

        result = result + lucky_text + other_text + overview_text
        return result