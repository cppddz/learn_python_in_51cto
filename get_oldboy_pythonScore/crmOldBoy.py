import urllib.request as ur
import http.cookiejar 
import urllib
# cookie = cookielib.CookieJar()
# handler=ur.HTTPCookieProcessor(cookie)
# opener = ur.build_opener(handler)
# response = opener.open('http://crm.oldboyedu.com/crm/grade/single/')

def getInfo(csrfmiddlewaretoken,qq):
    headers = {'User-Agent' :"Mozilla/5.0 (Windows NT 5.1; rv:46.0) Gecko/20100101 Firefox/46.0",
               #'Host' : "crm.oldboyedu.com",
               # 'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               # 'Referer':"http://crm.oldboyedu.com/crm/grade/single/",
               # 'Cookie':cookieTemp,
               # 'Connection':"keep-alive"
               } 
    postdata = {
        'csrfmiddlewaretoken':csrfmiddlewaretoken,
        'search_str':qq
    }

    postData = urllib.parse.urlencode(postdata).encode('utf-8') 
    request = urllib.request.Request(posturl, postData, headers)  
    response = urllib.request.urlopen(request)  
    text = response.read().decode('UTF-8')
    return text

def getCookie(cookie):
    cookieDist = {}
    for i in cookie:
        cookieDist[i.name]=i.value
    cookieTemp = ''
    for k in cookieDist:
        cookieTemp = k+'='+cookieDist[k]
    csrfmiddlewaretoken = cookieDist['csrftoken']
    return csrfmiddlewaretoken


def getQQ(filePath):
    qqDict = {}
    with open(filePath,'r') as f:
        num = 1
        for i in f.readlines():
            i = i.strip()
            if  i.endswith(','):
                qq = i.strip(',')
                qqDict[qq] = qq
            if not i:
                break
            qq,seq = i.split(',')
            qqDict[seq] = qq
    return qqDict
def run():
    import re,json,time
    print("程序初始化中...")
    posturl = 'http://crm.oldboyedu.com/crm/grade/single/'
    filePath = 'qq.txt'
    re_rule = re.compile('<tbody><tr>(.*?)</tr></tbody>')
    re_rule2 = re.compile('<td>(.*?)</td>')
    cj = http.cookiejar.LWPCookieJar()
    cookies_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookies_support,urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    print('获取cookie...')
    try :
      response = opener.open(posturl)
      csrfmiddlewaretoken = getCookie(cj)
    except:
      print("获取cookie失败")
    print('读取QQ号码...')
    try :
      qqDict = getQQ(filePath)
    except:
      print('读取qq信息失败')
      qqDict = None
    allScore = []
    if not qqDict :
      print("程序退出！")
      exit()
    print('爬取成绩开始，将需要一些时间，请勿关闭程序....')
    stratTime = time.time()
    for seq,qq in qqDict.items():
        #print("获取信息,qq号：",qq)
        try :
            headers = {'User-Agent' :"Mozilla/5.0 (Windows NT 5.1; rv:46.0) Gecko/20100101 Firefox/46.0",
                       #'Host' : "crm.oldboyedu.com",
                       # 'Accept':"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                       # 'Referer':"http://crm.oldboyedu.com/crm/grade/single/",
                       # 'Cookie':cookieTemp,
                       # 'Connection':"keep-alive"
                       } 
            postdata = {
                'csrfmiddlewaretoken':csrfmiddlewaretoken,
                'search_str':qq
            }

            postData = urllib.parse.urlencode(postdata).encode('utf-8') 
            request = urllib.request.Request(posturl, postData, headers)  
            response = urllib.request.urlopen(request)  
            text = response.read().decode('UTF-8')
        except:
          print("获取网页数据错误，qq号：",qq)
          break
        req = getScore(text,re_rule,re_rule2)
        req.insert(0,qq)
        req.insert(0,seq)
        allScore.append(req)
    endTime = time.time()
    print('数据已完成下载,用时：%s秒'%(endTime - stratTime))
    # for i in allScore:
    #   print(i)
    try:
        with open('result.txt','w') as f:
            json.dump(allScore,f)
    except:
        print('写入result.txt文件失败....')
def getScore(text,re_rule,re_rule2):
    import re

    text = re.sub('\s','',text)
    req = re.findall(re_rule,text)
    if not req:
        return []
    req = req[0]
    req = re.findall(re_rule2,req)
    return req

