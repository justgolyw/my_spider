#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
文章实体类
"""
class Article:
    def __init__(self,title, url, content= '', read_cnt = 0):
        """
        :param title: 文章标题
        :param url: 文章url
        :param content: 文章简介
        :param read_cnt: 文章阅读数
        """
        self.title = title
        self.url = url
        self.content = content
        self.read_cnt = read_cnt

    # 重写__str__方法
    def __str__(self):
        return u'文章：标题:《{0}》，阅读数：{1}，链接：{2}'.format(self.title,self.read_cnt,self.url)

