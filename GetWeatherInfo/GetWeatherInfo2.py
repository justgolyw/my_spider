#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging,requests,csv
from bs4 import BeautifulSoup

class GetWeatherInfo:
    def __init__(self):
        # 日志
        self.log = logging
        self.log.basicConfig(level=logging.INFO)

    # 获取soup
    def get_soup(self,url):
        # 消息请求头
        header = {
            'Accept': 'text/html,*/*,q=0.1',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) Apple'
        }
        response = requests.get(url,headers = header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,features='html.parser')
        return soup

    # 解析HTML页面，获取weather信息
    def get_weatherInfo(self,url):
        weather_all = []
        soup = self.get_soup(url)
        # 打印日志
        self.log.info('开始解析HTML页面......')
        # 找到天气信息
        weather_div = soup.find('div',class_='c7d')
        ul = weather_div.find('ul')
        li = ul.find_all('li')
        for day in li:
            # 每一天的天气信息
            weather = []
            # 日期
            date = day.find('h1').text
            weather.append(date)
            info = day.find_all('p')
            # 天气
            wea = info[0].text
            weather.append(wea)
            # 最高温度
            temp_high = info[1].find('span').text
            weather.append(temp_high)
            # 最低温度
            temp_low = info[1].find('i').text
            weather.append(temp_low)
            # 将每一天的天气信息添加到list保存
            weather_all.append(weather)
        return weather_all

    # 解析HTML页面，获取weather信息
    def get_weatherInfo2(self, url):
        weather_all = []
        soup = self.get_soup(url)
        # 打印日志
        self.log.info('开始解析HTML页面......')
        # 找到天气信息
        weather_div = soup.find('div', class_='c7d')
        ul = weather_div.find('ul')
        li = ul.find_all('li')
        for day in li:
            # 每一天的天气信息
            weather = []
            # 日期
            date = day.find('h1').text
            weather.append(date)
            # info = day.find_all('p')
            # 天气
            wea = day.find('p',class_ = 'wea').text
            weather.append(wea)
            temp = day.find('p', class_='tem')
            # 最高温度
            temp_high = temp.find('span').text
            weather.append(temp_high)
            # 最低温度
            temp_low = temp.find('i').text
            weather.append(temp_low)
            # 将每一天的天气信息添加到list保存
            weather_all.append(weather)
        return weather_all

    # 写入文件保存
    def write_to_csv(self,path,weatherInfo):
        """
        :param path: 保存路径
        :param weatherInfo: 天气信息
        :return:
        """
        with open(path,mode='w') as f:
            f_csv = csv.writer(f,delimiter = ',')
            # 将信息按行写入csv保存
            # 写入的对象一定要是一个可迭代对象
            f_csv.writerows(weatherInfo)
        self.log.info('写入文件成功')

    def write_to_txt(self,path,weatherInfo):
        i = 1
        with open(path,mode='w') as f:
            for weather in weatherInfo:

                f.write(str(i)+':')
                f.write(str(weather))
                f.write('\n')
                i += 1



    def run(self, url):

        # 获取天气信息
        weather_all = self.get_weatherInfo2(url)
        self.write_to_csv('weather2.csv',weather_all)
        self.write_to_txt('weather2.txt',weather_all)
        # 打印日志
        for weather in weather_all:
            self.log.info(weather)


if __name__ == '__main__':
    url = 'http://www.weather.com.cn/weather/101020100.shtml'
    getWeatherInfo = GetWeatherInfo()
    getWeatherInfo.run(url)











