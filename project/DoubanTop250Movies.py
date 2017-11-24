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
    a = soup('span','title')#通过观察网页的源代码可以发现电影的名字被保存在标签名为span，属性为title的标签中
    for i in a: 
        s = i.string
        if u'\u4e00' <= str(s) <= u'\u9fff':  #通过find_all函数找到的标签中含有非电影名的标签，其中全中文的标签为电影名
            ls.append(str(s))
        else:
            continue
#打印最终结果
def printList(ls):
    tplt = '{0:^8}\t{1:{2}^10}'
    print(tplt.format('排名','名字',chr(12288)))  #由于填充时用英文的空格填充导致不能够正常居中对齐，因此用中文的空格chr（12288）进行填充
    num = 0
    for i in ls:
        print(tplt.format(num+1,ls[num],chr(12288)))
        num += 1

def main():
    page = 0
    ls = []
    while page < 11:
        url = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='  #豆瓣的翻页处理是通过url的start参数进行翻页的，每页有25个电影，共有10页
        html = getHTMLText(url)
        getMovies(ls,html)
        page += 1
    printList(ls)

if __name__ == '__main__':
    main()
