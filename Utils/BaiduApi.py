import requests
from Utils import utils, SQLiteUtils
import time
import os
def get_token():
    url = 'https://openapi.baidu.com/oauth/2.0/token'
    params = {
        'grant_type': 'client_credentials',
        'client_id': 'IpskvYso5W3E4kPV6dVMHH3N',
        'client_secret': '1an3P3dSQC6Qxh5Mh2eU86Z4MsFP33Ak'
    }
    res = requests.get(url=url, params=params)
    return res.json()


def is_token_expired():
    data = SQLiteUtils.get_token()
    get_token_time = data[2]
    current_time = int(time.time())
    interval = (current_time - get_token_time)/3600/24
    if interval <= 30:
        return data[1]
    else:
        new_data = get_token()
        new_data['get_token_time'] = current_time
        SQLiteUtils.refresh_token(new_data)
        return new_data['access_token']



def text2audio():
    file_name = os.getcwd() +'/audioSave/'+ str(int(time.time())) + '.mp3'
    text = utils.get_chp()
    access_token = is_token_expired()
    url = 'https://tsn.baidu.com/text2audio'
    params = {
        'tex' : text.encode('utf-8'),
        'tok' : access_token,
        'cuid': 'bfb934374a1c4625ada18fc366111c4d',
        'ctp' : 1,
        'lan' : 'zh',
        'per' : 4
    }
    res = requests.get(url=url,params=params)
    with open(file_name,'wb') as f:
        f.write(res.content)
    return file_name


if __name__ == '__main__':
    print(is_token_expired())
