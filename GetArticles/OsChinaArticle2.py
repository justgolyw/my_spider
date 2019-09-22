#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
文章处理类,相关的逻辑在该类中实现
"""
import csv
import operator
import os,sys
import time
import requests,logging
from bs4 import BeautifulSoup
import openpyxl

from GetArticles.Article import Article


class OsChinaArticle:
    def __init__(self):
        # 日志
        # self.log = logging
        # # 设置logger格式 formatter = logging.Formatter(fmt=None, datefmt=None)
        # # format = logging.Formatter(fmt="%(asctime)s - %(message)s", datefmt='%a, %d %b %Y %H:%M:%S')
        # # 设置日志级别
        # self.log.basicConfig(level=logging.INFO,
        #                     format='%(asctime)s %(filename)s %(levelname)s %(message)s',
        #                     datefmt='%a, %d %b %Y %H:%M:%S',
        #                     filename = 'myapp.log', filemode='w')

        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)
        # 设置logger格式 formatter = logging.Formatter(fmt=None, datefmt=None)
        format = logging.Formatter(fmt="%(asctime)s - %(message)s", datefmt='%a, %d %b %Y %H:%M:%S')
        # 创建 handler 处理器
        # fh = logging.FileHandler(filename, mode='a', encoding=None, delay=False)
        hander = logging.FileHandler('article.log',mode='w',encoding="UTF-8")
        hander2 = logging.StreamHandler(sys.stderr)
        hander2.setFormatter(format)
        # hander 添加格式
        hander.setFormatter(format)
        self.log.addHandler(hander)
        self.log.addHandler(hander2)

        # 文章编号
        self.file_line_num = 1

    # 根据url获取BeautifulSoup 对象
    def get_soup(self,url):
        # 请求头
        header = {
            'Accept': 'text/html,*/*,q=0.1',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) Apple',
            'Host': 'www.oschina.net'
        }

        # headers = header 为关键字参数
        response = requests.get(url,headers = header)
        # 获取HTML页面
        soup = BeautifulSoup(response.text, features='html.parser')
        return soup

    # 通过BeautifulSoup 解析HTML页面，获取文章相关信息
    def get_articles(self,url):

        article_list = []
        soup = self.get_soup(url)
        self.log.info(u'开始解析 HTML页面...')
        # 找到所有的文章
        article_divs = soup.find_all('div',class_='item blog-item')
        for article_div in article_divs:
            temp = []
            # 文章content主体
            content_div = article_div.find('div',class_= 'content')
            head_div = content_div.find('a',class_='header')
            # 文章标题
            title = head_div['title']
            temp.append(title)
            # 文章url
            url = head_div['href']
            temp.append(url)
            # 文章描述
            description_str = content_div.find('div',class_ = 'description').find('p',class_ = 'line-clamp')
            if description_str is None:
                continue
            description = description_str.text
            # 文章阅读数
            read_count_div = content_div.find('div',class_ = 'extra').find('div',class_ = 'ui horizontal list').find('div',class_ = 'item')
            # 获取兄弟节点：find_next_sibling (阅读数在第三个兄弟节点处)
            read_count = read_count_div.find_next_sibling('div',class_ = 'item').find_next_sibling('div',class_ = 'item').text
            temp.append(read_count)
            # 创建文章对象，保存到集合
            # article = Article(title,url,description,read_count)
            article_list.append(temp)
            # article_list.append(article)
            # 打印log
            # self.log.info(u'文章：标题《{0}》，阅读数：{1}，链接：{2}'.format(title,read_count,url))
        # print(article_list)
        return article_list

    # 处理文章阅读数
    def handler_read_count(self,article_list):
        """
        因为文章的阅读数如果超过 1000 的话，就用 K 来表示，
        为了在后面筛选指定阅读数的文章，所以需要进行处理，把 K 转换为 1000：
        """
        if article_list is None or len(article_list) == 0:
            self.log.info(u'文章列表为空')
            return
        for article in article_list:
            # read_count_str = article.read_cnt
            read_count_str = article[2]

            read_count = 0
            if isinstance(read_count_str,str):
                if read_count_str.endswith('K'):
                    read_count_str = read_count_str[:-1] # 去掉K
                    read_count = int(float(read_count_str)*1000)
                else:
                    read_count = int(read_count_str)

            article[2] = read_count


    def get_article_by_read_count_sort(self,article_list,min_read_cnt):
        """
        :param article_list: 文章列表
        :param min_read_cnt: 最小阅读数
        :return:
        """
        if article_list is None or len(article_list) == 0:
            self.log.info('文章列表为空')
            return
        result_list = []
        for article in article_list:
            if int(article[2]) >= min_read_cnt:

                result_list.append(article)
        # 排序(reverse=True:倒序)
        # result_list.sort(key=lambda Article: Article.read_cnt, reverse=True)
        result_list.sort(key=operator.itemgetter(2),reverse=True)
        # print(result_list)
        return result_list

    # 写入txt文件保存
    def write_to_txt(self,article_list,file_path):
        """
        :param article_list: 文章列表
        :param file_path: 保存路径
        :return:
        """
        self.file_line_num = 1
        with open(file_path, mode='w', errors='ignore') as f:
        # f = open(file_path + "/article.txt", "a")
            for article in article_list:
                # 转换为str
                article_str = str(article)
                f.write('('+ str(self.file_line_num)+')'+article_str)
                f.write('\n')# 换行
                f.write('---------------------------------------------------------')
                f.write('\n')  # 换行
                self.file_line_num += 1
                time.sleep(0.2)
        # f.close()# 最后一定要关闭文件
        print('write to txt success')

    # 写入csv文件保存
    def write_to_csv(self, article_list,file_path):
        """
        :param article_list:文章列表
        :param file_path: 保存路径
        :return:
        """
        with open(file_path, mode='w',errors='ignore') as f:

            f_csv = csv.writer(f)
            f_csv.writerows(article_list)
        print('write to csv success')

    def write_to_excel(self,article_list,file_path):
        # 创建workbook
        wb = openpyxl.Workbook()
        # 激活sheet
        sheet = wb.active
        sheet.title = 'articleList'
        sheet['A1'] = '标题'
        sheet['B1'] = '链接'
        sheet['C1'] = '阅读数'
        # 写入数据
        for i in range(2, 2 + len(article_list)):
            for j in range(1, 1 + len(article_list[0])):
                sheet.cell(row=i, column=j).value = article_list[i - 2][j - 1]
        # 保存
        wb.save(file_path)


    def run(self, min_read_count, pageSize):
        # url = "https://www.oschina.net/blog?classification=428640"
        for page in range(1,pageSize+1):
            self.log.info('第{0}页##########################################'.format(page))
            page_url = 'https://www.oschina.net/blog?classification=428640&p='+str(page)
            # 获取每一页所有文章
            articleList = self.get_articles(page_url)
            # 对阅读数进行处理
            self.handler_read_count(articleList)
            # 筛选阅读数大于等于指定值，并按阅读数从高到低排序
            article_list = self.get_article_by_read_count_sort(articleList, min_read_count)
            # file_path = os.path.join(os.path.join(os.getcwd(),'..'),'article.txt')
            # file_path = 'article.txt'
            # self.write_to_txt(article_list,file_path)
            file_path = 'article.csv'
            file_path2 ='article.xlsx'
            self.write_to_csv(article_list,file_path)
            self.write_to_excel(article_list,file_path2)
            # 打印日志
            for article in article_list:
                self.log.info(article)


if __name__ == '__main__':
    osArticle = OsChinaArticle()
    # url = "https://www.oschina.net/blog?classification=428640"
    pageSize = 2
    min_read_count = 1000
    osArticle.run(min_read_count,pageSize)






