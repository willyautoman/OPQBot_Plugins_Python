import datetime
import time
from PIL import Image,ImageFont,ImageDraw


def Draw(det):
    font = ImageFont.truetype('sucai/Arial.ttf', 60)
    font_fu = ImageFont.truetype('sucai/Arial.ttf', 55)
    times = time.localtime()
    title = '{}年{}月{}日 {}'.format(times[0], times[1], times[2], det['result']['city'])
    # 打开底版图片
    imageFile = "sucai/forcast.jpg"
    im1 = Image.open(imageFile)
    # 在图片上添加日期、城市
    draw = ImageDraw.Draw(im1)
    draw.text((15, 50), title, (0, 0, 0), font=font)
    draw = ImageDraw.Draw(im1)

    # 在图片中添加实时天气
    draw = ImageDraw.Draw(im1)
    draw.text((200, 472), det['result']['realtime']['info'], (0, 0, 0), font=font)
    draw.text((200, 590), det['result']['realtime']['temperature'] + '°C', (0, 0, 0), font=font)
    draw.text((200, 703), det['result']['realtime']['humidity'] + '%', (0, 0, 0), font=font)
    draw.text((200, 816), det['result']['realtime']['direct'], (0, 0, 0), font=font)
    draw.text((200, 929), det['result']['realtime']['power'], (0, 0, 0), font=font)
    draw.text((200, 1042), det['result']['realtime']['aqi'], (0, 0, 0), font=font)
    draw = ImageDraw.Draw(im1)

    # 在图片中添加天气预报（每五行为一天）
    draw.text((710, 195), det['result']['future'][0]['date'], (0, 0, 0), font=font)
    draw.text((790, 285), det['result']['future'][0]['weather'], (0, 0, 0), font=font_fu)
    draw.text((790, 395), det['result']['future'][0]['temperature'].replace('℃', '°C'), (0, 0, 0), font=font_fu)
    draw.text((790, 505), det['result']['future'][0]['direct'], (0, 0, 0), font=font_fu)
    draw.text((790, 615), det['result']['future'][0]['wid']['day'] + '级', (0, 0, 0), font=font_fu)

    draw.text((1210, 195), det['result']['future'][1]['date'], (0, 0, 0), font=font)
    draw.text((1300, 285), det['result']['future'][1]['weather'], (0, 0, 0), font=font_fu)
    draw.text((1300, 395), det['result']['future'][1]['temperature'].replace('℃', '°C'), (0, 0, 0), font=font_fu)
    draw.text((1300, 505), det['result']['future'][1]['direct'], (0, 0, 0), font=font_fu)
    draw.text((1300, 615), det['result']['future'][1]['wid']['day'] + '级', (0, 0, 0), font=font_fu)

    draw.text((1710, 195), det['result']['future'][2]['date'], (0, 0, 0), font=font)
    draw.text((1810, 285), det['result']['future'][2]['weather'], (0, 0, 0), font=font_fu)
    draw.text((1810, 395), det['result']['future'][2]['temperature'].replace('℃', '°C'), (0, 0, 0), font=font_fu)
    draw.text((1810, 505), det['result']['future'][2]['direct'], (0, 0, 0), font=font_fu)
    draw.text((1810, 615), det['result']['future'][2]['wid']['day'] + '级', (0, 0, 0), font=font_fu)

    draw.text((710, 715), det['result']['future'][3]['date'], (0, 0, 0), font=font)
    draw.text((790, 805), det['result']['future'][3]['weather'], (0, 0, 0), font=font_fu)
    draw.text((790, 915), det['result']['future'][3]['temperature'].replace('℃', '°C'), (0, 0, 0), font=font_fu)
    draw.text((790, 1025), det['result']['future'][3]['direct'], (0, 0, 0), font=font_fu)
    draw.text((790, 1135), det['result']['future'][3]['wid']['day'] + '级', (0, 0, 0), font=font_fu)

    draw.text((1210, 715), det['result']['future'][4]['date'], (0, 0, 0), font=font)
    draw.text((1300, 805), det['result']['future'][4]['weather'], (0, 0, 0), font=font_fu)
    draw.text((1300, 915), det['result']['future'][4]['temperature'].replace('℃', '°C'), (0, 0, 0), font=font_fu)
    draw.text((1300, 1025), det['result']['future'][4]['direct'], (0, 0, 0), font=font_fu)
    draw.text((1300, 1135), det['result']['future'][4]['wid']['day'] + '级', (0, 0, 0), font=font_fu)
    today = datetime.date.today().strftime("%Y%m%d")
    name = today + '{}.jpg'.format(det['result']['city'])
    im1.save('weather_pic/'+name)
    return name
