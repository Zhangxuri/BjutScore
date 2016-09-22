
#coding=utf-8

#-*- coding: UTF-8 -*-
import urllib2
import cookielib
import urllib
import re
import getpass

name=""
username = raw_input("Please input your student ID:")
password = getpass.getpass()
PostUrl = "http://gdjwgl.bjut.edu.cn/default2.aspx"
CaptchaUrl = "http://gdjwgl.bjut.edu.cn/CheckCode.aspx"
# 验证码地址和post地址
cookie = cookielib.CookieJar()
handler = urllib2.HTTPCookieProcessor(cookie)
opener = urllib2.build_opener(handler)

def Print(Score_html):  # print the result
    str = r"<td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.?)</td>"
    str = re.compile(str)
    result = {}
    subject = []
    a = str.findall(Score_html)
    for i in a:
        for j in range(15):
            subject.append(i[j])
        result[subject[3]] = subject
        subject = []

    for i in result.keys():
        j = result[i]
        # print j
        print '%-10s%-2s%-10s%-8s%6s%8s%10s%6s%6s%5s%10s%-10s%-15s%s%s' % tuple(j)
        print " "

def getName(loginPage):  # get the name
    Sname = r'<span id="xhxm">(.+)同学</span>'
    Sname = re.compile(Sname)
    return Sname.findall(loginPage)[0]

def getVIEW(Page):  # Get viewststes for login page

    view = r'name="__VIEWSTATE" value="(.+)" '
    view = re.compile(view)
    return view.findall(Page)[0]

def getSecretCode():
 # 将cookies绑定到一个opener cookie由cookielib自动管理
 picture = opener.open(CaptchaUrl).read()
 # 用openr访问验证码地址,获取cookie
 local = open('image.jpg', 'wb')
 local.write(picture)
 local.close()
 # 保存验证码到本地
 SecretCode = raw_input('输入验证码： ')
 # 打开保存的验证码图片 输入
 return SecretCode

'''模拟登录'''
Page = urllib2.urlopen('http://gdjwgl.bjut.edu.cn/default2.aspx').read()
postData = urllib.urlencode({
'__VIEWSTATE': getVIEW(Page),
'txtUserName': username,
'TextBox2': password,
'txtSecretCode': getSecretCode(),
'RadioButtonList1': '学生',
'Button1': '',
'lbLanguage': '',
'hidPdrs': '',
'hidsc': '',
})
# 根据抓包信息 构造表单
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Connection': 'keep-alive',
'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
# 根据抓包信息 构造headers
# 生成post数据 ?key1=value1&key2=value2的形式
request = urllib2.Request(PostUrl, postData, headers)
# 构造request请求

try:
 result = opener.open(request).read().decode('gb2312').encode("utf-8")
 # 由于该网页是gb2312的编码，所以需要解码
 print ("SUCCESS")
 name=getName(result)
 # 打印登录后的页面
except urllib2.HTTPError, e:
 print e.code

# cookie重构,很关键
for i in cookie:
 Cookie = i.name + "=" + i.value

head = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'gdjwgl.bjut.edu.cn',
        'Cookie': Cookie,
        'Origin': 'http://gdjwgl.bjut.edu.cn',
        'Referer':'http://gdjwgl.bjut.edu.cn/xscjcx.aspx?xh='+username,
        'Upgrade-Insecure-Requests': 1,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    }

getdata = urllib.urlencode({
        'xh': username,
        'xm': name,
        'gnmkdm': 'N121605'
    })

MyRequest = urllib2.Request('http://gdjwgl.bjut.edu.cn/xscjcx.aspx?' + getdata, None,
                                head)  # According to this page ,we can get the viewstats
loginPage = unicode(opener.open(MyRequest).read(), 'gb2312').encode("utf-8")
dataOfFinal = urllib.urlencode({
         '__EVENTTARGET':'',
         '__EVENTARGUMENT':'',
         '__VIEWSTATE': getVIEW(loginPage),
         'btn_zcj': '历年成绩',
         'hidLanguage':'',
         'ddlXN':'',
         'ddlXQ':'',
         'ddl_kcxz':''
    })
MyRequest = urllib2.Request('http://gdjwgl.bjut.edu.cn/xscjcx.aspx?' + getdata, dataOfFinal, head)  # Score's page
html = opener.open(MyRequest)
result = unicode(html.read(), 'gb2312').encode("utf-8")
Print(result)
