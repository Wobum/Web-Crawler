import requests
from bs4 import BeautifulSoup

#获取url的文本
def getHTMLText(url):
    try:
        r = requests.get(url,timeout = 30,headers = {'user-agent':'Mozilla/5.0'})
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return '爬取链接失败'

#通过美味汤库解析url生成的文本，获得电影的名字
def getMovies(ls,html):
    soup = BeautifulSoup(html,'html.parser')
    li = soup('li')
    n = 20#从第20个‘li’标签开始保存电影信息
    while n < 45: #共有45个‘li'标签
        l1 = [] 
        a = li[n]('span','title') #电影的名字
        b = li[n]('span','other') #电影的别名
        for t in a:
            l1 =[]
            t1 = str(a[0].string)   #‘title’标签第一项保存电影中文名
            l1.append(t1)
            if len(a) != 1: #第二项保存电影原名
                t2 = str(a[1].string.split('\xa0')[-1])
                l1.append(t2)
            else:#没有原名说明这个电影为大陆拍摄，用其中文名作为原名
                l1.append(t1)
        t3 = str(b[0].string).split('\xa0')[-1]
        l1.append(t3.lstrip())
        ls.append(l1)
        n += 1
        
        
#打印最终结果
def printList(ls,ln):      #lnv表示控制打印前ln个电影
    tplt = '{0:^8}\t{1:{4}^10}\t{2:<60}\t{3:<50}'
    print(tplt.format('排名','中文名','原名','别名',chr(12288)))  #由于填充时用英文的空格填充导致不能够正常居中对齐，因此用中文的空格chr（12288）进行填充
    num = 0
    for i in ls:
        while num < ln:
            print(tplt.format(num+1,ls[num][0],ls[num][1],ls[num][2],chr(12288)))
            num += 1

def main():
    page = 0
    ls = []
    n = input('你想要打印前多少的电影:')
    while page < 10:
        url = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='  #豆瓣的翻页处理是通过url的start参数进行翻页的，每页有25个电影，共有10页
        html = getHTMLText(url)
        getMovies(ls,html)
        page += 1
    printList(ls,int(n))

if __name__ == '__main__':
    main()
