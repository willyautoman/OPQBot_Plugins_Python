import base64
import datetime
import json
import os
import random
import re
import threading
import time
from time import sleep
import datetime
import iotbot.decorators as deco
import requests
import schedule
from iotbot import IOTBOT, Action, GroupMsg, EventMsg
from Utils import utils, SQLiteUtils, BaiduApi, setuUtil, ciyunUtil, weatherUtil


bot = IOTBOT(1328382485, log_file=True)
action = Action(bot,queue=True,queue_delay=2)


def getGroupList():
    GroupID = []
    groupList = action.get_group_list()
    TroopList = groupList['TroopList']
    for group in TroopList:
        GroupID.append(group['GroupId'])
    return GroupID


def sent_wyy():
    print("网抑云定时任务执行成功")
    file = os.listdir('wyy')[random.randint(0, 9)]
    groupList = getGroupList()
    text = SQLiteUtils.get_netease()
    with open('wyy//' + file, 'rb') as f:
        coding = base64.b64encode(f.read()).decode()
        for group in groupList:
            action.send_group_pic_msg(toUser=group, content=text, picBase64Buf=coding)
            sleep(1)
    return


def sent_morning():
    print("早安定时任务执行成功")
    file = os.listdir('morning')[random.randint(0, 10)]
    text = SQLiteUtils.get_morning()
    groupList = getGroupList()
    print(text)
    with open('morning//' + file, 'rb') as f:
        coding = base64.b64encode(f.read()).decode()
        for group in groupList:
            action.send_group_pic_msg(toUser=group, content=text, picBase64Buf=coding)
            sleep(1)
    return


def sent_ciyun():
    print("开始生成词云")
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime("%Y%m%d")  # 昨天的日期
    groupList = getGroupList()
    for group in groupList:
        filename = str(group) + '_' + yesterday + '.txt'
        pic_base64 = ciyunUtil.create_ciyun(filename)
        if pic_base64 is not None:
            action.send_group_pic_msg(toUser=group, content="昨日本群词云已生成，请查收~[PICFLAG]", picBase64Buf=pic_base64)
        # print(pic_base64)


def schedule_test():
    Content = time.asctime(time.localtime(time.time()))
    action.send_friend_text_msg(toUser=1127738407, content=Content)
    print("执行成功")


def schedule_threading():
    while True:
        schedule.run_pending()
        # print("refresh")
        sleep(1)


@bot.on_group_msg
def get_record(msg: GroupMsg):
    today = datetime.date.today().strftime("%Y%m%d")
    if msg.MsgType == 'TextMsg':
        filename = str(msg.FromGroupId) + '_' + today + '.txt'
        with open('record/' + filename, 'a+')as f:
            f.write(msg.Content + '\n')
            f.close()


#机器人聊天，如有需要，自己取消注释
# @bot.on_group_msg
# @deco.only_this_msg_type("TextMsg")
# def auto_reply(msg: GroupMsg):
#     rand = random.randint(0, 40)
#     print(rand)
#     if rand % 25 == 0:  #自己计算触发概率
#         question = msg.Content
#         reply = main.chat(question)
#         action.send_group_text_msg(msg.FromGroupId, reply, atUser=msg.FromUserId)


@bot.on_group_msg
@deco.in_content("昨日词云")
def send_ciyun(msg: GroupMsg):
    print("开始生成词云")
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = (today - oneday).strftime("%Y%m%d") # 昨天的日期
    groupList = getGroupList()
    for group in groupList:
        filename = str(group) + '_' + yesterday + '.txt'
        pic_base64 = ciyunUtil.create_ciyun(filename)
        action.send_group_pic_msg(toUser=group, content="昨日本群词云已生成，请查收~[PICFLAG]", picBase64Buf=pic_base64)
    return


@bot.on_group_msg
@deco.in_content("色图")
def send_setu(msg: GroupMsg):
    action.send_group_pic_msg(toUser=msg.FromGroupId, content='30S后销毁该消息，请快点冲，谢谢', picUrl='http://127.0.0.1:8080/getContent')

@bot.on_group_msg
@deco.in_content("(.*?)市天气")
def send_waether(msg:GroupMsg):
    action.send_group_text_msg(toUser=msg.FromGroupId,content='正在查询中，请稍后······')
    pattern = re.compile(r'(.*?)市天气')
    m = pattern.match(msg.Content)
    city = m.group(1)
    weather = utils.GetWeather(city)
    File_name = weatherUtil.Draw(weather)
    with open('weather_pic/'+File_name, 'rb')as f:
        coding = base64.b64encode(f.read()).decode()
        action.send_group_pic_msg(toUser=msg.FromGroupId, picBase64Buf=coding)


@bot.on_group_msg
def revoke_msg(msg: GroupMsg):
    if msg.FromUserId == 1328382485 and msg.MsgType == 'PicMsg':
        Content = json.loads(msg.Content)['Content']
        if Content == '30S后销毁该消息，请快点冲，谢谢':
            print(Content)
            time.sleep(30)
            action.revoke_msg(msg.FromGroupId, msg.MsgSeq, msg.MsgRandom)

@bot.on_group_msg
@deco.in_content(".github")
@deco.in_content("github")
def send_proj(msg:GroupMsg):
    text = '本机器人源码：'+'https://github.com/willyautoman/OPQBotPlugins-Python'+ '\n看后记得star一下哦'
    action.send_group_text_msg(toUser=msg.FromGroupId,content=text)

@bot.on_group_msg
@deco.in_content("彩虹屁")
def send_chp(a: GroupMsg):
    text = utils.get_chp()
    print(text)
    action.send_group_text_msg(toUser=a.FromGroupId, content=text)



@bot.on_group_msg
def send_shanzhao(a: GroupMsg):
    if a.MsgType == 'PicMsg' and 'GroupPic' not in a.Content:
        Contents = json.loads(a.data.get('Content'))
        action.send_group_pic_msg(toUser=a.FromGroupId, content='震惊！居然有人敢在这个群里发闪照！', picUrl=Contents['Url'],
                                      fileMd5=Contents['FileMd5'])

@bot.on_group_msg
@deco.in_content("我想对你说")
def send_voice(a: GroupMsg):
    file_name = BaiduApi.text2audio()
    with open(file_name, 'rb') as f:
        coding = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
        print('本地base64转码~')
        voice_base64 = coding.decode()
        action.send_group_voice_msg(toUser=a.FromGroupId, voiceBase64Buf=voice_base64)
        return


@bot.on_group_msg
@deco.in_content("QQ测运势")
def send_qqcys(msg: GroupMsg):
    text = utils.get_cjx(msg)
    print(text)
    action.send_group_text_msg(toUser=msg.FromGroupId, content=text,atUser=msg.FromUserId)


@bot.on_group_msg
def send_xingzuo(a: GroupMsg):
    pattern = re.compile(r'(.*?座)(.*?)运势')
    m = pattern.match(a.Content)
    if m is not None:
        texts = utils.get_xzys(m.group(1), m.group(2))
        print(texts)
        for text in texts:
            action.send_group_text_msg(toUser=a.FromGroupId, content=text)

#新成员入群欢迎
@bot.on_event
def on_people_in_group(event: EventMsg):
    if event.MsgType == 'ON_EVENT_GROUP_JOIN' and event.FromUin == '#####':   #此处填入需要发送欢迎的群号

        UserName = event.EventData['UserName']
        UserID = event.EventData['UserID']
        with open('bqb//' + str(random.randint(1,161)) + '.jpg', 'rb') as f:
            coding = base64.b64encode(f.read()).decode()
            text = "\n[表情109][表情109]欢迎2020级萌新：%s入群[表情109][表情109]\n入群请先修改群名片（如：2020-呼市-张三）\n 有什么问题请尽管提问，在线的大二、大三的学长学姐们会很热♂情的帮你们解答的"%UserName
            action.send_group_pic_msg(toUser=event.FromUin,content=text,atUser=UserID,picBase64Buf=coding)

@bot.on_group_msg
@deco.in_content("获取个人信息")
def get_detail(msg:GroupMsg):
    print(action.get_user_info(userID=msg.FromUserId))
    print(type(action.get_user_info(userID=msg.FromUserId)))


if __name__ == "__main__":
    schedule.every().day.at("00:00").do(sent_wyy)
    schedule.every().day.at("08:00").do(sent_ciyun)
    schedule.every().day.at("07:00").do(sent_morning)
    thread_schedule = threading.Thread(target=schedule_threading)
    thread_schedule.start()
    bot.run()
