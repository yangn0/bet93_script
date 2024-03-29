import requests
import re
import time
import os
import datetime
import json
import base64

from functools import wraps

main_url=input("输入网站主域名：")
# main_url="93193j.com"
# www.93cp16.com
key_token=input("输入key_token：")
# 36a9fc3a3b65
request_timeout = (10, 20)

class CatchException:

    def __init__(self, times=5, wait=3):
        self.times = times
        self.wait = wait

    def __call__(self, func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            for _ in range(self.times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f'{func.__name__}失败：{args} {kwargs} {e}')
                    time.sleep(self.wait)
            else:
                return False
        return wrapped_function


def generate():
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/home/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'affid=null;ssid1=cafc972161ab0ded340b71b7b4a841e4',
    }
    response = requests.get(f'https://{main_url}/web/rest/captcha/generate', headers=headers, verify=False, timeout=(6.05, 6.05))
    print(response.text)
    data = response.json()
    image_data = base64.b64decode(data['result']['backgroundImage'].split(',')[1])
    positionY = data['result']['positionY']
    uuid = data['result']['uuid']
    with open('./code.png', 'wb') as f:
        f.write(image_data)
    return positionY, uuid

def base64_api(uname, pwd, typeid):
    with open('./code.png', 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data, verify=False, timeout=(6.05, 6.05)).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


def validate(positionX, positionY, uuid):
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'content-type': 'application/json;charset=UTF-8',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': f'https://{main_url}',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/home/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cookie': 'affid=null;ssid1=cafc972161ab0ded340b71b7b4a841e4',
    }
    json_ = {
        'positionX': positionX,
        'positionY': positionY,
        'uuid': uuid
    }
    response = requests.post(f'https://{main_url}/web/rest/captcha/validate', headers=headers, json=json_, verify=False, timeout=(6.05, 6.05))
    print(response.text)
    data = response.json()
    cryptograph = data['result']['cryptograph']
    code = data['result']['code']
    return cryptograph, code

@CatchException(2, 2)
def ssid():
    headers = {
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    s = requests.Session()
    response = s.get(f'https://{main_url}/ssid1?url=/member/agreement?_OLID_=0ce6293789f17d45360a775508b8ab5e362a42d7', headers=headers, verify=False)
    return dict(s.cookies.items())



# def cashlogin(session: requests.Session, account='!guest!', password='!guest!', force_login=False):
#     token = ''
#     ssid1 = ''
#     random = ''
#     with open('token.txt', mode='r', encoding='utf8') as file:
#         token = file.read().strip()
#     with open('ssid1.txt', mode='r', encoding='utf8') as file:
#         ssid1 = file.read().strip()
#     with open('random.txt', mode='r', encoding='utf8') as file:
#         random = file.read().strip()
#     return token, ssid1, random




# 登陆接口
@CatchException(20, 6)
def cashlogin(session: requests.Session, account='!guest!', password='!guest!', force_login=False):
    os.makedirs('account', exist_ok=True)
    os.makedirs(os.path.join('account', 'bet'), exist_ok=True)

    path = ''
    if not account or not password:
        path = os.path.join('account', 'bet', 'guest.txt')
        account = '!guest!'
        password = '!guest!'
    else:
        path = os.path.join('account', 'bet', f'{account}#{password}.txt')
    if not force_login and os.path.exists(path):
        token = ''
        with open(path, mode='r', encoding='utf-8') as file:
            token = file.read().strip()
            return token
    if 'guest' not in account:
        positionY, uuid = generate()
        positionX = int(base64_api(uname='sheli19888', pwd='yang1314', typeid=33)) - 9
        cryptograph, code = validate(positionX=positionX, positionY=positionY, uuid=uuid)
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': f'https://{main_url}',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/home/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'affid=null',
    }
    if 'guest' in account:
        url = f'https://{main_url}/web/rest/cashlogin?account={account}&password={password}'
    else:
        url = f'https://{main_url}/web/rest/cashlogin?account={account}&password={password}&code={code}&cryptograph={cryptograph}'
    response = session.post(url, headers=headers, verify=False)
    print(response.text)
    t = response.json()['message'].split('=')[1]

    with open(path, mode='w', encoding='utf-8') as file:
        file.write(t)

    return t
#

# 最新一期开奖结果
@CatchException(10, 1)
def lastResult(session: requests.Session, lottery: str, token: str, ssid1: str, random: str):
    headers = {
        'authority': f'{main_url}',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        #'cookie': 'c8f15dac3426=b2d853b1965dfcaff3bda9139db2d4b266635d06; ssid1=e65e7eed118acca44a6e455bb59ea741; random=7258; affid=null; token=b2d853b1965dfcaff3bda9139db2d4b266635d06',
        'referer': f'https://{main_url}/member/index',
        'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT={lottery}; affid=null; token={token}; ssid1={ssid1}',
    }
    params = (
        ('lottery', lottery),
        ('_', f'{round(time.time()*1000)}'),
    )
    response = session.get(f'https://{main_url}/member/lastResult', headers=headers, timeout=request_timeout, verify=False, params=params)
    print(response.text)
    response = response.json()
    # return {
    #     'draw_number': response['drawNumber'],
    #     'result': response['result'].split(',')
    # }

    r = {
        'last_result': {
            'issue': response['drawNumber'],
            'result': response['result'].split(',')
        },
        f"{response['drawNumber']}": response['result'].split(',')
    }

    hr = history_record(session=session, lottery=lottery, token=token, ssid1=ssid1, random=random)
    print("hr %s"%len(hr))
    if hr:
        for k, v in hr.items():
            r[k] = v['result']
    print("lastResult完成")
    return r


# 下一期 期号
@CatchException(3, 0)
def period(session: requests.Session, lottery: str, token: str, ssid1: str, random: str):
    headers = {
        'authority': f'{main_url}',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': f'https://{main_url}/member/load?lottery=XYFT&page=lm',
        'sec-ch-ua': '^\\^.Not/A)Brand^\\^;v=^\\^99^\\^, ^\\^Google',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\\^Windows^\\^',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT={lottery}; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    params = (
        ('lottery', lottery),
        ('_', f'{round(time.time() * 1000)}'),
    )
    response = session.get(f'https://{main_url}/member/period', headers=headers, timeout=request_timeout, verify=False, params=params)
    #print(response.text)
    response = response.json()
    return {
        'cpqh': response['drawNumber'],
        'current_time': int(response['currentTime'])/1000,
        'ndate': int(response['closeTime']),

    }


@CatchException(1, 0)
def bet(session: requests.Session, json_: dict, token: str, ssid1: str, random: str):
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'accept': '*/*',
        'content-type': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': f'https://{main_url}',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/member/index',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT={json_["lottery"]}; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    #去掉虚拟投注
    json_copy=json_.copy()
    json_['bets']=list()
    for i in json_copy['bets']:
        if(i['amount']>=2):
            json_['bets'].append(i)
        else:
            print("虚拟下注",i)
            
    response = session.post(f'https://{main_url}/member/bet', json=json_, headers=headers, timeout=(20, 20), verify=False)
    print(response.text)
    response = response.json()
    try:
        return {
            'balance': float(response['account']['balance']),
            'betting': response['account']['betting'],
            'profit': float(response['account'].get('result', 0))
        }
    except:
        return {
            'balance': -1,
        }


@CatchException(2, 2)
def account(session: requests.Session, token: str, ssid1: str, random: str):
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/member/index',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT=AULUCKY10; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    response = session.get(f'https://{main_url}/member/account?_={round(time.time() * 1000)}', headers=headers, timeout=request_timeout, verify=False)
    #print(response.text)
    response = response.json()
    # return {
    #     'balance': float(response['balance']),
    #     'betting': response['betting'],
    #     'profit': float(response.get('result', 0))
    # }
    return float(response['balance'])

def draw(session: requests.Session, cardid: str, drawcode: str, drawamount: int, token: str, ssid1: str, random: str):
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'accept': '*/*',
        'content-type': 'application/json',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': f'https://{main_url}',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/member/index',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT=AULUCKY10; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': f'https://{main_url}',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://{main_url}/member/payment/withdrawal',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'affid=null; {key_token}={token}; _skin_=red; defaultLT=SGFT; _bindSecQue=true; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    data = {
        'drawamount': str(drawamount),
        'cardid': str(cardid),
        'drawcode': str(drawcode),
        'type': '0',
        'transId': '',
        'code': '',
        'currency': ''
    }
    response = session.post(f'https://{main_url}/member/payment/draw', headers=headers, data=data, verify=False)
    #print(response.text)
    r = ''
    try:
        r = response.json()
    except:
        r = '无返回结果，检查卡号和提现密码后，重试'
    return r


@CatchException(2, 2)
def dresult(session: requests.Session, lottery: str, token: str, ssid1: str, random: str):
    today = datetime.datetime.now()
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'iframe',
        'referer': f'https://{main_url}/member/dresult?lottery=AULUCKY10&date={today.strftime("%Y-%m-%d")}&table=1',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT=AULUCKY10; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }

    if lottery == 'AULUCKY5' or lottery == 'SSCJSC' or lottery== 'SGSSC':
        reponse = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={today.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
        pattern = re.compile(r'<td class="name"><span class="b.+>(\d+)</span></td>')
        #print(reponse.text)
        result = []
        today_result = pattern.findall(reponse.text)
        result = result + today_result
        previous = 10
        period_num = len(result) / 5
        if True:
            yesterday = today + datetime.timedelta(-1)
            reponse = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={yesterday.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
            #print(reponse.text)
            yesterday_result = pattern.findall(reponse.text)
            result = result + yesterday_result
        # result = list(map(lambda item: int(item), result))
        history = []
        for index in range(0, len(result), 5):
            history.append(result[index:index + 5])
        #print(history)

        return history
    else:
        reponse = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={today.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
        pattern = re.compile(r'<td class="name ballname"><span class="b.+>(\d+)</span></td>')
        #print(reponse.text)
        result = []
        today_result = pattern.findall(reponse.text)
        result = result + today_result
        previous = 10
        period_num = len(result) / 10
        if True:
            yesterday = today + datetime.timedelta(-1)
            reponse = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={yesterday.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
            #print(reponse.text)
            yesterday_result = pattern.findall(reponse.text)
            result = result + yesterday_result
        # result = list(map(lambda item: int(item), result))
        history = []
        for index in range(0, len(result), 10):
            history.append(result[index:index + 10])
        #print(history)

        return history


@CatchException(1, 0)
def history_record(session: requests.Session, lottery: str, token: str, ssid1: str, random: str):
    today = datetime.datetime.now()
    yesterday = today + datetime.timedelta(-1)

    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'iframe',
        'referer': f"https://{main_url}/member/dresult",
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT=AULUCKY10; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }

    if lottery == 'AULUCKY5' or lottery == 'SSCJSC' or lottery== 'SGSSC':
        reponse1 = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={today.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
        reponse2 = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={yesterday.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False)
        text = reponse1.text + reponse2.text
        #print(text)
        # 期号
        pattern = re.compile(r'<td class="period">(\d+?)</td>')
        period = pattern.findall(text)
        #print(period)

        # 号码
        pattern = re.compile(r'<td class="name"><span class="b.+>(\d+?)</span></td>')
        result = pattern.findall(text)
        history = []
        for index in range(0, len(result), 5):
            history.append(result[index:index + 5])
        #print(history)
        #return dict(zip(period, history))
        data = dict()
        for i, (p, h) in enumerate(zip(period, history)):
            data[p] = {
                'result': h,
                'next_issue': None if i == 0 else period[i - 1],
                'index': i
            }
        return data
    else:
        reponse1 = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={today.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False,timeout=request_timeout)
        reponse2 = session.get(url=f'https://{main_url}/member/dresult?lottery={lottery}&date={yesterday.strftime("%Y-%m-%d")}&table=1', headers=headers, verify=False,timeout=request_timeout)

        text = reponse1.text + reponse2.text
        #print(text)

        # 期号
        pattern = re.compile(r'<td class="period">(\d+?)</td>')
        period = pattern.findall(text)
        #print(period)

        # 号码
        pattern = re.compile(r'<td class="name ballname"><span class="b.+>(\d+?)</span></td>')
        result = pattern.findall(text)
        history = []
        for index in range(0, len(result), 10):
            history.append(result[index:index + 10])
        #print(history)
        data = dict()
        for i, (p, h) in enumerate(zip(period, history)):
            data[p] = {
                'result': h,
                'next_issue': None if i == 0 else period[i-1],
                'index': i
            }
        return data


if __name__ == '__main__':
    # s = requests.Session()
    # #cashlogin(session=s, force_login=True)
    # r = history_record(session=s, lottery='LUCKYSB', token='d04e021c29bd43091e9b39706d7347d26b1cf781',ssid1="6c91cc1091d0ab63efee057fba5a2117",random="9026")
    # print(r)
    # pass
    token="d04e021c29bd43091e9b39706d7347d26b1cf781"
    ssid1="6c91cc1091d0ab63efee057fba5a2117"
    random=""
    headers = {
        'authority': f'{main_url}',
        'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'iframe',
        'referer': "https://93193j.com/member/dresult",
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{key_token}={token}; _skin_=red; defaultLT=AULUCKY10; affid=null; token={token}; ssid1={ssid1}; random={random}',
    }
    r=requests.get("https://93193j.com/member/dresult?lottery=LUCKYSB",headers=headers)

    print(r.text)