# -*- coding: utf-8 -*-
# author: 'boliang'
# date: 2018/3/2 11:10

import re
import requests
from lxml import etree
import jieba
import matplotlib
import matplotlib.pyplot as plt


class Solution(object):
    def __init__(self, url):
        # 爬取团队介绍的页面
        res = requests.get(url)
        # 采集介绍信息
        selector = etree.HTML(res.text)
        content = selector.xpath("//div[@class='piece-body p-lg clearfix']/p/text()")
        content = re.sub('[\\\\x|\s|，|）|（|,|:|：|！|!|、|。]', '', ''.join(content)).strip()

        # jieba 分词
        jieba.add_word('学号')
        jieba.add_word('Python')
        jieba.add_word('MySQL')
        jieba.add_word('JavaScript')
        jieba.add_word('HTML')
        jieba.add_word('Java')
        self.__words = list(jieba.cut(content))
        self.__record_set = set(self.__words)
        self.__record_dict = {}
        for word in self.__record_set:
            self.__record_dict[word] = self.__words.count(word)

        print(self.__record_dict)

    # 画出词频统计图（柱状图）
    def draw_image(self):
        zhfont = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc')
        plt.xticks(fontproperties=zhfont, fontsize=16)
        plt.xlabel(u'词汇', fontproperties=zhfont, fontsize=20)
        plt.ylabel(u'数量', fontproperties=zhfont, fontsize=20)
        X = [key for key in self.__record_dict.keys() if self.__record_dict[key] > 2]
        Y = list(map(lambda key:self.__record_dict[key], X))
        plt.bar(X, Y)
        plt.title(u'词频统计', fontproperties=zhfont,fontsize=20)
        plt.show()

    # 统计所有词的数量
    def show_cal_words(self):
        print('总共有{0}个词(包括英文术语)'.format(len(self.__record_set)))
        for key, value in self.__record_dict.items():
            print('({0}) 的数量为: {1}'.format(key, value))


if __name__ == '__main__':
    Solution('http://www.yzhiliao.com/course/65').show_cal_words()



