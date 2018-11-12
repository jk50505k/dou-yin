import requests
import os
from bs4 import BeautifulSoup
import re
import time

path='抖音'#下载路径
max_cursor=0
headers={'User-Agent': 'Aweme/25010 CFNetwork/902.2 Darwin/17.7.0'}
downloadList=[]
nameList=[]
share_link='http://v.douyin.com/RQN2Qf/'
share_lin=input('请输入分享链接：')

def getParam(link):
    global uid,dytk
    r=requests.get(link,headers=headers)
    soup=BeautifulSoup(r.content,'html.parser')
    script=soup.find_all('script',attrs={'type':'text/javascript'})
    uid_t = re.findall(r'uid\: \"[0-9]+\"', str(script[2]))
    dytk_t = re.findall(r"dytk\: \'[A-Za-z0-9_]+\'",str(script[2]).replace('\\',''))
    uid=re.findall(r'\d+',uid_t[0])[0]
    dytk=re.findall(r"\'\w+\'",dytk_t[0])[0].replace('\'','')
    #print(uid)
    return uid,dytk

def getpage(url):
    global max_cursor
    r=requests.get(url,headers=headers)
    result=r.json()
    #print(result)
    getUrl(result['aweme_list'])
    if  result['has_more'] == 1:
        max_cursor=result['max_cursor']
        url = 'https://www.amemv.com/aweme/v1/aweme/post/?iid=42373740908&device_id=50710506156&os_api=18&app_name=aweme&channel=App%20Store&idfa=C2E933BD-A0F9-4D0A-AEC5-A66084B45F26&device_platform=iphone&build_number=25010&vid=9FF1B946-950F-4E2F-B899-FBE327304747&openudid=af16bf3bf0261000061c28b9c00ad87266c42175&device_type=iPhone9,1&app_version=2.5.0&version_code=2.5.0&os_version=11.4.1&screen_width=750&aid=1128&ac=WIFI&user_id=' + uid + '&count=21&max_cursor=' + str(
            max_cursor) + '&aid=1128&_signature=yUxVXRASksp2OqS76wPuE8lMVU&dytk=' + dytk
        getpage(url)#递归调用

def getUrl(urlList):
    for i in urlList:
        downloadList.append(i['video']['play_addr']['url_list'][0])
        nameList.append(i['share_info']['share_desc'])

def download(url,filename):
    r=requests.get(url,headers=headers)
    with open(os.path.join(path,(filename+'.mp4')),'wb') as fd:
        fd.write(r.content)




if __name__ == '__main__':
    if not os.path.exists(path):
        os.makedirs(path)
    getParam(share_link)
    url = 'https://www.amemv.com/aweme/v1/aweme/post/?iid=42373740908&device_id=50710506156&os_api=18&app_name=aweme&channel=App%20Store&idfa=C2E933BD-A0F9-4D0A-AEC5-A66084B45F26&device_platform=iphone&build_number=25010&vid=9FF1B946-950F-4E2F-B899-FBE327304747&openudid=af16bf3bf0261000061c28b9c00ad87266c42175&device_type=iPhone9,1&app_version=2.5.0&version_code=2.5.0&os_version=11.4.1&screen_width=750&aid=1128&ac=WIFI&user_id=' + uid + '&count=21&max_cursor=' + str(
        max_cursor) + '&aid=1128&_signature=BUQoGhAaXs-6Mtn8HVj0aQVEKA&dytk=' + dytk
   
    getpage(url)
    for i in range(len(downloadList)):
        print(nameList[i]+':'+downloadList[i])
        download(downloadList[i], nameList[i])
   
        
