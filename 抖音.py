import requests
import os
from bs4 import BeautifulSoup
import re

path='抖音'
max_cursor=0
count=0
headers={'User-Agent': 'Aweme/25010 CFNetwork/902.2 Darwin/17.7.0'}
downloadList=[]
nameList=[]
share_link=''#将分享链接粘贴到这


def getParam(link):
    global uid,dytk
    r=requests.get(link,headers=headers)
    soup=BeautifulSoup(r.content,'html.parser')
    script=soup.find_all('script',attrs={'type':'text/javascript'})
    uid_t = re.findall(r'uid\: \"[0-9]+\"', str(script[2]))
    dytk_t = re.findall(r"dytk\: \'[A-Za-z0-9_]+\'",str(script[2]).replace('\\',''))
    uid=re.findall(r'\d+',uid_t[0])[0]
    dytk=re.findall(r"\'\w+\'",dytk_t[0])[0].replace('\'','')
    return uid,dytk


def getpage(url):
    global max_cursor
    r=requests.get(url,headers=headers)
    result=r.json()
    getUrl(result['aweme_list'])
    if  result['has_more'] == 1:
        max_cursor=result['max_cursor']
        url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id=' + uid + '&count=21&max_cursor=' + str(
            max_cursor) + '&aid=1128&_signature=yUxVXRASksp2OqS76wPuE8lMVU&dytk=' + dytk
        getpage(url)

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
    url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id=' + uid + '&count=21&max_cursor=' + str(
        max_cursor) + '&aid=1128&_signature=BUQoGhAaXs-6Mtn8HVj0aQVEKA&dytk=' + dytk
    getpage(url)
    #print(downloadList)

    for i in range(len(downloadList)):
        print('Downloading:'+nameList[i])
        download(downloadList[i],nameList[i])
