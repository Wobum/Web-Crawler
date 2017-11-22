import requests
import os
url = input('输入图片url链接:')
root = 'F:/pics/'
path = root + url.split('/')[-1]
try :
	if not os.path.exists(root):
		os.mkdir(root)
	if not os.path.exists(path):
		r = requests.get(url)
		r.raise_for_status
		with open(path,'wb') as f:
			f.write(r.content)
			print('文件保存成功')
	else:
		print('图片已存在')
except:
	print('爬取失败')
