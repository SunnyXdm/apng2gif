# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import json, requests

class AnimatedPNGToGIF:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    def getGIF(self, resp):
        soup = BeautifulSoup(resp.content, 'lxml')
        data = {}
        url = soup.find('form')['action'] + '?ajax=true'
        for input in soup.find_all('input'):
            try:
                data[input['name']] = input['value']
            except:
                continue
        r = self.session.post(url, data=data, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')
        return 'https:' + soup.find('img', alt='[apng-to-gif output image]')['src']

    def apngByURL(self, url):
        host = 'https://ezgif.com/apng-to-gif?' + urlencode({'url': url})
        r = self.session.get(host, headers=self.headers)
        return self.getGIF(r)

    def apngByFile(self, path):
        data = {
            'new-image-url': ''
        }
        files = {'new-image': open(path,'rb')}
        host = 'https://s6.ezgif.com/apng-to-gif'
        r = self.session.post(host, data=data, headers=self.headers, files=files)
        return self.getGIF(r)
