#-*- coding: UTF-8 -*-
import json
import sys
import re
import urllib2
import urllib
import requests
import cookielib
import time
import pytesseract
from PIL import Image
import requests,os,re,smtplib,time
from urllib2 import urlopen
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup

## 这段代码是用于解决中文报错的问题
reload(sys)
sys.setdefaultencoding("utf8")
#####################################################
# 获取验证码
# http://learn.open.com.cn/Account/ValidatePic?0.11095544709114713
ValidatePicUrl='http://learn.open.com.cn/Account/ValidatePic?0.11095544709114713'
# 用验证码登录 +加上面获取的验证码
# http://learn.open.com.cn/Account/UnitLogin?t=134&loginName=huangbqopen&passWord=open1609&validatenum=73217&rememberMe=1
LoginUrl='http://learn.open.com.cn/Account/UnitLogin?t=134&loginName=huangbqopen&passWord=open1609&rememberMe=1&validatenum='
#主界面 http://learn.open.com.cn/StudentCenter/Index
IndexUrl='http://learn.open.com.cn/StudentCenter/Index'
#点击
ClickUrl='http://pv.open.com.cn/click.php?type=heatmap&clickTarget=1&logVisitId=676416e2-bbfe-420e-8161-d0e24de599c5-1480476177758&logBtsVal=676416e2-bbfe-420e-8161-d0e24de599c5&logUserid=huangbqopen&pageId=1480478024946-71835420633215114509135219839237&logUrl=%2Flearn.open.com.cn%2FStudentCenter%2FIndex&logcharset=UTF-8&logChannel=100200&logmx=185&logmy=364&ver=2015021001&time='
myRequests = requests.Session()
headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Cookie':'ASP.NET_SessionId=mrw4nq0c3w0usfxpxrd2wo01; Hm_lvt_686401bd1a1f7184252b460af0f4337e=1480411732; Hm_lpvt_686401bd1a1f7184252b460af0f4337e=1480411732; LmsForm=Name=huangbqopen&Pwd=open1609&RememberMe=1',
            'Host':'learn.open.com.cn',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

myRequests.headers.update(headers)
# 模糊替换
rep = {'O': '0',
       'I': '1',
       'L': '1',
       'Z': '2',
       'S': '8',
       'Q': '0',
       '}': '7',
       '*': '',
       'E': '6',
       ']': '0',
       '`': '',
       'B': '8',
       '\\': '',
       '.': '',
       ',':'',
       ' ': '',
       '(1': '0',
       '’': '',
       '‘':''
       }
CodesImg = os.path.join(os.getcwd(), 'imgcode.jpg')
class openlogin:
    def __init__(self):
        self.name = ''
        self.passwprd = ''
        self.domain = ''
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))

        self.codeImg = 'imgcode_1.jpg'
        self.Im = self._openImg(self.codeImg.capitalize())
        self.w, self.h = self.Im.size
    def _openImg(self, name):
        try:
            im = Image.open(name)
            return im
        except:
            print '[!] Open %s failed' % name
            exit()
    def getcode(self):
        #通过接口获取图片
        r = myRequests.get(url=ValidatePicUrl)
        f = open(CodesImg, 'wb')
        f.write(r.content)
        f.close()

        # 把彩色图像转化为灰度图像
        im = Image.open('imgcode.jpg')
        imgry = im.convert('L')

        # 图片去噪
        threshold = 120
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        out = imgry.point(table, '1')
        out.save('imgcode_1.jpg')
        #保存cookie
        out.show()
    def pIx(self):
            data = self.Im
            w = self.w
            h = self.h
            try:
                for x in xrange(1, w - 1):
                    if x > 1 and x != w - 2:
                        left = x - 1
                        right = x + 1

                    for y in xrange(1, h - 1):
                        up = y - 1
                        down = y + 1

                        if x <= 2 or x >= (w - 2):
                            data.putpixel((x, y), 255)

                        elif y <= 2 or y >= (h - 2):
                            data.putpixel((x, y), 255)

                        elif data.getpixel((x, y)) == 0:
                            if y > 1 and y != h - 1:
                                up_color = data.getpixel((x, up))
                                down_color = data.getpixel((x, down))
                                left_color = data.getpixel((left, y))
                                left_down_color = data.getpixel((left, down))
                                right_color = data.getpixel((right, y))
                                right_up_color = data.getpixel((right, up))
                                right_down_color = data.getpixel((right, down))

                                if down_color == 0:
                                    if left_color == 255 and left_down_color == 255 and \
                                                    right_color == 255 and right_down_color == 255:
                                        data.putpixel((x, y), 255)
                                        data.save("imgcode_2.jpg", "png")
                                        return 'imgcode_2.jpg'
                                elif right_color == 0:
                                    if down_color == 255 and right_down_color == 255 and \
                                                    up_color == 255 and right_up_color == 255:
                                        data.putpixel((x, y), 255)
                                        data.save("imgcode_3.jpg", "png")
                                        return 'imgcode_3.jpg'
                            if left_color == 255 and right_color == 255 \
                                    and up_color == 255 and down_color == 255:
                                data.putpixel((x, y), 255)
                        else:
                            pass
                        data.save("imgcode_4.jpg", "png")
                        return 'imgcode_4.jpg'
            except:
                return False
    def readcode(self,imgname):
        # 获取验证码
        image = Image.open(imgname)
        try:
           vcode = pytesseract.image_to_string(image)
           for r in rep:
              vcode = vcode.replace(r, rep[r])
           return vcode
        except:
            return '000000'
    def login(self,code):
        url = LoginUrl+ str(code)
        r1= myRequests.get(url)
        r2 = myRequests.get(url)
        jsonData = json.loads(r2.content)
        if jsonData['status'] == 0:
            print '登录成功'
            return  True
        else:
            print '登录失败'
            return  False
    def openindex(self):
        print myRequests.get(IndexUrl).content
        print myRequests.get(ClickUrl+str("%d" %(time.time()*1000))).content

        # print html.content
        #
        # req = urllib2.Request(IndexUrl,'', headers=headers)
        # response = urllib2.urlopen(req)
        # self.operate = self.opener.open(req)
        # url = self.operate.geturl()
        # thePage = response.read()
        # print thePage

    def timer(self,n):
        while True:
            print time.strftime('%Y-%m-%d %X', time.localtime())
            openlogin().openindex()
            time.sleep(n)
if __name__ == '__main__':
        # 获取验证码
        I = openlogin()
        I.getcode()

        #验证码手动输入吧
        code=input()
        I.login(code)

        #控制在线，3分钟刷新一次
        I.timer(10)

        #打开课程















