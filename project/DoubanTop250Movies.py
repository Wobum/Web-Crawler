import requests
import re
import os
from bs4 import BeautifulSoup

class getDouBanTop250Movies(object):

        
    #获取url链接的源代码
    def getHTMLText(self,url):
        try:
            r = requests.get(url,timeout = 30,headers = {'user-agent':'Mozilla/5.0'})
            r.raise_for_status
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return '爬取链接失败'

    #通过正则表达式提取出链接源代码中与电影有关的信息
    def getMovies(self,l,html):
        soup = BeautifulSoup(html,'html.parser')
        li = soup('li')
        num = 20
        ls = []
        while num < 45:
            title = li[num]('span','title')
            ls.append(title[0].string)  #电影名字
            num += 1
        rank = re.findall(u'<em class="">(.*?)</em>',html) #电影排名
        other_title = re.findall(u'<span class="other">&nbsp;/&nbsp;(.*?)</span>',html)#电影别名
        director = re.findall(u'导演:(.*?)nbsp',html) #导演
        protagonist = re.findall(u'主(.*?)<br>',html) #主演
        there  = re.findall(u' (.*?)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*)',html)#包含上映年份，制作国家，电影类型
        start = re.findall(u'<span class="rating_num" property="v:average">(.*?)</span>',html)#电影评分
        people = re.findall(u'<span>(.+?)人评价',html)#评分人数
        file_review = re.findall(u'<span class="inq">(.*?)</span>',html) #简短影评
        l.append(rank)
        l.append(ls)
        l.append(other_title)
        l.append(director)
        l.append(protagonist)
        l.append(there)
        l.append(start)
        l.append(people)
        l.append(file_review)
            
    #保存最终结果
    def saveMovies(self,l):      
        root = 'C:\\Users\\81421\\Desktop\\Web Crawler\\project\\'
        path = root + '豆瓣Top250电影信息.txt'
        if not os.path.exists(root):
             os.mkdir(root)
        if not os.path.exists(path):
            try:
                page = 0
                while page < 10:
                    num = 0
                    while num < 25:
                        with open(path,'a',encoding = 'utf-8') as f:
                            f.write('电影排名：'+l[0+(page*9)][num]+'\r\n')
                            f.write('电影名字：'+l[1+(page*9)][num]+'\r\n')
                            f.write('电影别名：'+l[2+(page*9)][num]+'\r\n')
                            #f.write('电影导演：'+l[3+(page*9)][num]+'\r\n')   由于豆瓣电影Top250页面有的电影导演和主演会由于显示字数问题而没有被显示，如果抓取会导致程序运行错误
                            #f.write('电影主'+l[4+(page*9)][num]+'\r\n')
                            f.write('电影上映年份：'+str(l[5+(page*9)][num][0]).strip()+'\r\n')
                            f.write('电影制作国家：'+l[5+(page*9)][num][1]+'\r\n')
                            f.write('电影电影类型：'+l[5+(page*9)][num][2]+'\r\n')
                            f.write('电影评分：'+l[6+(page*9)][num]+'分'+'\r\n')
                            f.write('电影评分人数：'+l[7+(page*9)][num]+'人评分'+'\r\n')
                            f.write('简短影评：'+l[8+(page*9)][num]+'\r\n')
                            f.write('\r\n')
                        print('Top',(num+1)+25*page,'电影信息保存成功！')
                        num += 1
                    page += 1
            except:
                print('保存电影信息出错')
        else:
            print('电影信息已存在！')
           
            
                  
    def main(self):
        page = 0
        l = []
        while page < 10:
            print('正在爬取第',page+1,'页信息，请稍等...')
            url = 'https://movie.douban.com/top250?start=' + str(page*25) + '&filter='  #豆瓣的翻页处理是通过url的start参数进行翻页的，每页有25个电影，共有10页
            html = self.getHTMLText(url)
            self.getMovies(l,html)
            page += 1
        #print(len(l))
        self.saveMovies(l) 


DouBanSpider = getDouBanTop250Movies()
DouBanSpider.main()
