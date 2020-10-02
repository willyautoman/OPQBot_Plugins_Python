# coding:utf-8
import jieba  # 分词
import matplotlib.pyplot as plt  # 数据可视化
import numpy  as np  # 科学计算
from PIL import Image  # 处理图片
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS  # 词云
from io import BytesIO
import base64
import os
def create_ciyun(file_name):
    # 打开文本
    if os.path.exists('record/' + file_name):
        textfile = open('record/' + file_name, encoding='utf-8').read()  # 读取文本内容
        wordlist = jieba.cut_for_search(textfile)
        space_list = " ".join(wordlist)  # 链接词语
        backgroud = np.array(Image.open("Utils/backgroud.jpg"))  # 背景图片
        mywordcloud = WordCloud(mask=backgroud,  # 写字用的背景图，从背景图取颜色
                                stopwords=STOPWORDS,  # 停止的默认词语
                                font_path="Utils/simkai.ttf",  # 字体
                                max_font_size=200,  # 最大字体尺寸
                                random_state=50,  # 随机角度
                                scale=2).generate(space_list)
        plt.imshow(mywordcloud)  # 显示词云
        plt.axis("off")  # 关闭保存
        save_file = BytesIO()
        plt.savefig(save_file, format='png')

        # 转换base64并以utf8格式输出
        file_base64 = base64.b64encode(save_file.getvalue()).decode()
        return file_base64

