#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
分页下载百度贴吧图片
"""
import logging,requests,csv
from bs4 import BeautifulSoup
import os

# 下载图片
class GetPicture:
    def __init__(self):

        # 日志
        self.log = logging
        self.log.basicConfig(level=logging.INFO)
        self.index = 1 # 图片编号

    # 获取soup
    def get_soup(self,url):
        # 消息请求头
        header = {
            'Accept': 'text/html,image/webp,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip,deflate,sdch,br',
            'Accept-language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) Apple',
        }
        response = requests.get(url,headers = header)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,features='html.parser')
        return soup

    # 解析HTML页面
    def get_picture(self,url):
        # 创建一个保存图片的文件夹
        os.makedirs('Images', exist_ok=True) # 只支持python3
        # index = 1 # 图片编号
        soup = self.get_soup(url)
        # 打印日志
        # self.log.info('开始解析HTML页面......')
        all_img = soup.find_all('img', class_='BDE_Image')

        for img in all_img:
            self.log.info('下载图片......')
            img_url = img['src']
            img_name = str(self.index)+'.jpg'
            # 下载图片
            img_content = requests.get(img_url).content
            # 保存图片
            with open(os.path.join('Images',img_name),mode='wb') as f:
                f.write(img_content)
            self.index += 1

    def get_picture_by_pages(self,url,pageNum):
        for page in range(1,pageNum+1):
            self.log.info('正在下载第{0}页的图片......'.format(page))
            page_url = url + '?pn='+str(page)
            self.get_picture(page_url)


if __name__ == '__main__':
    url = 'http://tieba.baidu.com/p/2460150866'
    getPic = GetPicture()
    getPic.get_picture_by_pages(url,10)












