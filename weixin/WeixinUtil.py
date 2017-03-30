import requests
import config

class WeixinApi():

    def get_token(self):
        payload_access_token = {
            'grant_type': 'client_credential',
            'appid': config.WEIXIN_APPID,
            'secret': config.WEIXIN_APPSECRET
        }
        token_url = 'https://api.weixin.qq.com/cgi-bin/token'
        res = requests.get(url=token_url,params=payload_access_token)
        result = res.json()
        return result['access_token']

    def get_media_id(self):
        upload_url = 'https://api.weixin.qq.com/cgi-bin/media/upload'
        payload_img = {
            'access_token': self.get_token(),
            'type': 'image'
        }
        data = {'media': open(config.MEDIA_MZI_PATH+r'\mzitu1.jpg', 'rb')}
        r = requests.post(url=upload_url, params=payload_img, files=data)
        result = r.json()
        return result

    def get_media_count(self):
        url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount'
        payload_img = {
            'access_token': self.get_token()
        }
        r = requests.post(url=url, params=payload_img)
        result = r.json()
        return result
