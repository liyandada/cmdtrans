#!/usr/bin/env python3
import json
import random
import hashlib
from urllib import parse
import http.client
import os
import sys


class BaiduTranslate:
    def __init__(self,fromLang,toLang):
        self.url = "/api/trans/vip/translate"
        self.appid="20210304000714744" #申请的账号
        self.secretKey = 'mItMrtLR0RhTFarWkr1B'#账号密码
        self.fromLang = fromLang
        self.toLang = toLang
        self.salt = random.randint(32768, 65536)

    def BdTrans(self,text):
        sign = self.appid + text + str(self.salt) + self.secretKey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        myurl = self.url + \
                '?appid=' + self.appid + \
                '&q=' + parse.quote(text) + \
                '&from=' + self.fromLang + \
                '&to=' + self.toLang + \
                '&salt=' + str(self.salt) + \
                '&sign=' + sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            html = response.read().decode('utf-8')
            html = json.loads(html)
            dst = html["trans_result"][0]["dst"]
            return  True , dst
        except Exception as e:
            return False , e
if __name__=='__main__':
    BaiduTranslate_test = BaiduTranslate('en','zh')
    cmdname = sys.argv[1]
    str_tldr = "tldr "
    cmdrun = str_tldr + cmdname
    
    var = os.popen(cmdrun).read()
    processFunc = lambda s: " ".join(s.split())
    strin = var.replace('\n',"\\n")
    print(var)
    Results = BaiduTranslate_test.BdTrans(strin)#要翻译的词组
    strin2=Results[1]
    strin3=strin2.replace('\\n', "\n")
    allstrin= " "
    i = 0
    for i in range(len(var.split('\n'))-1):
        allstrin +=var.splitlines()[i]
        allstrin += '\n'
        allstrin += strin3.splitlines()[i]
        allstrin += '\n'

    print(allstrin)
