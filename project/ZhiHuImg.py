import requests
import re
import os

#用于获得url文本的函数
def getHTMLText(url):
        try:                
                r = requests .get(url,timeout = 30,headers = {'user-agent':'Mozilla/5.0'})
                r.raise_for_status
                r.encoding = r.apparent_encoding
                return r.text
        except:
                return '爬取失败'
        
#用于获得图片的url链接的函数，并将图片的url链接保存在一个列表中
def getUrl(l,html):
        regex = re.compile(r'data-actualsrc=".*?">')
        imagelt = regex.findall(html)
        for i in imagelt:
                url = i.split('=')[-1][1:-2]
                l.append(str(url))
                
#通过获得的图片url链接将图片保存在制定的文件夹中
def savePic(l):
        root = 'F:/pics/朱茵/'
        for url in l:
                path = root + url.split('/')[-1]
                try:
                        if not os.path.exists(root):
                                os.mkdir(root)
                        if not os.path.exists(path):
                                r = requests.get(url)
                                r.raise_for_status
                                with open(path,'wb') as f:
                                        f.write(r.content)
                                        print('图片保存成功')
                        else:
                                print('图片已存在')
                except:
                        print('爬取失败')
                        
def main():
        l = []
        url = 'https://www.zhihu.com/question/30360455'
        html = getHTMLText(url)
        getUrl(l,html)
        savePic(l)
        print('程序运行完毕')

if __name__ == '__main__':
        main()
