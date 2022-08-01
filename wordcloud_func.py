# 词云生成函数，可简单通过from wordcloud_func import * 来调用
import jieba
from wordcloud import WordCloud
import os
import sys
import re
from PIL import Image
import numpy as np

def stopwordslist():
     stopwords = [line.strip() for line in open('dict/chinsesstoptxt.txt',encoding='UTF-8').readlines()]
     return stopwords
 
def chinese_jieba(text):
    jieba.load_userdict("dict/words.txt")
    wordlist = jieba.cut(text,HMM=True)
    stopwords = stopwordslist()
    outstr = ''
    # 去停用词
    for word in wordlist:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += "."
    #wordlist_for_cy = " ".join(wordlist)
    return outstr


def ciyun(path, file_name, font_path):
    filefullname = os.path.join(path, file_name)
    #backgroud_Image = np.array(Image.open('mask.png'))
    with open(filefullname, encoding="utf-8")as file:
        text = file.read()
        text = chinese_jieba(text)
        wordcloud = WordCloud(font_path=font_path,
                              background_color="white", width=600, scale=4,
                              height=600, max_words=200, min_font_size=8, contour_color='steelblue').generate(text)
        pngpath = os.path.join(path, "png")
        isExists = os.path.exists(pngpath)
        if not isExists:
            os.makedirs(pngpath)
        pngfile_split = os.path.splitext(file_name)
        pngfile = pngfile_split[0]+".png"
        pngfullfile = os.path.join(pngpath, pngfile)
        print("\""+pngfullfile+"\""+"    writing")
        wordcloud.to_file(pngfullfile)
        print("\"" + pngfullfile + "\"" + "    written")
    return
