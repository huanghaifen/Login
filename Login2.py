#! /usr/bin/env python
# coding:utf-8

import sys
import re
import urllib2
import urllib
import requests
import cookielib

## 这段代码是用于解决中文报错的问题
reload(sys)
sys.setdefaultencoding("utf8")
#####################################################
# 登录
loginurl = 'http://oa.aisidi.com/logon.aspx'
logindomain = 'aisidi.com'


class Login(object):
    def __init__(self):
        self.name = ''
        self.passwprd = ''
        self.domain = ''

        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setLoginInfo(self, username, password, domain):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        self.domain = domain

    def login(self):
        '''登录网站'''
        #注意一下如果是aspx的请求，要加上一些奇怪的请求头。
        loginparams = {'txtUsername': self.name, 'txtPassword': self.pwd,'btnSignin':'登录','__VIEWSTATE':'/wEPDwUKMTAzMzQ2ODc4Mw8WAh4EVk51bQUEODE3MhYEAgMPZBYCAgcPDxYCHghJbWFnZVVybAUaL1ZhbGlkYXRlQ29kZS5hc3B4P3ZtPTgxNzJkZAIFDw9kFgIeA3NyYwUuUVJDb2RlSW1nLzMyNWFjM2Y0ZWE5NzRkMzk5MDc4Njk3ZmE3YzJhYWU5LnBuZ2RkfA7Jk5jnINHzzPoJiZ6JpJx3+gthdQjkwAJDibkOvVk=','__VIEWSTATEGENERATOR':'5A2128B1','__EVENTVALIDATION':'/wEdAASY15BrapSZmbdbmCJ3RBr/VK7BrRAtEiqu9nGFEI+jB3Y2+Mc6SrnAqio3oCKbxYaCysx15DoHQO+p6WIO0/CMT88heDjl7u6+ChpqnSKa0+Wy0XZNX2jhM0Rw0EO52GA='}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.57 Safari/537.36'}
        req = urllib2.Request(loginurl, urllib.urlencode(loginparams))
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        url=self.operate.geturl()
        print url
        thePage = response.read()
        print thePage


if __name__ == '__main__':
    userlogin = Login()
    username = 'huanghaifen'
    password = '329481'
    domain = logindomain
    userlogin.setLoginInfo(username, password, domain)
    userlogin.login()