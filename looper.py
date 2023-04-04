#from api import findFjkjhmList, loginWzDf, loginGuest, getDownTimeAndQh, putLottery, getHyje
from bet_api import cashlogin, lastResult, period, account, bet,history_record
import time
import requests
import threading
from location import Location,write_month_excel
import datetime,sys

input1=int(input("1极速飞艇 2幸运飞艇 3SG飞艇 4极速赛车:"))
day_num=int(input("要分析的天数："))
if(input1==1):
    lottery="LUCKYSB"
    print("极速飞艇")
elif(input1==2):
    lottery="XYFT"
    print("幸运飞艇")
elif(input1==3):
    lottery="SGFT"
    print("SG飞艇")
elif(input1==4):
    lottery="PK10JSC"
    print("极速赛车")

class Looper:

    def __init__(self, delete_all_item,get_plan, get_amount, get_win_back, get_account, set_issue, set_result, set_next_issue, get_lottery_profit, set_lottery_profit, stop_running, get_win_stop, get_lose_stop,
                 set_err_msg, get_one_out_end, set_one_out_end, set_balance, insert_item, set_item, write_config, get_out_end, set_out_end):
        self.get_plan = get_plan  # [['1', ['1', '2', '大']], ['1', ['1', '2', '大']]]
        self.get_amount = get_amount  # [[1, 3, 5], [33, 44, 55], [111, 222, 333]]
        self.get_win_back = get_win_back  # [6, 2]
        self.get_account = get_account  # {
        #     'username': '',
        #     'password': '',
        # }
        self.set_issue = set_issue
        self.set_result = set_result
        self.set_next_issue = set_next_issue
        self.get_lottery_profit = get_lottery_profit
        self.set_lottery_profit = set_lottery_profit
        self.stop_running = stop_running
        self.get_win_stop = get_win_stop
        self.get_lose_stop = get_lose_stop
        self.set_err_msg = set_err_msg
        self.get_one_out_end = get_one_out_end
        self.set_one_out_end = set_one_out_end
        self.set_balance = set_balance
        self.insert_item = insert_item
        self.delete_all_item=delete_all_item
        self.set_item = set_item
        self.write_config = write_config
        self.get_out_end = get_out_end
        self.set_out_end = set_out_end

        self.location_list = []
        self.session = requests.Session()
        self.last_bet_issue = ''  # 最近一期下注的期号
        self.start_ts = 0  # 上一次的登陆时间

        self.location_created_id = 0

        self.can_create_location = True

        self.flag = False
        threading.Timer(0, self.loop).start()
        #self.loop()

    def loop(self):
        self.logic2()
        print("完成")
    
    def logic2(self):
        ssid1="cafc972161ab0ded340b71b7b4a841e4"
        random_=""
        token = cashlogin(session=self.session, account=self.get_account()['username'], password=self.get_account()['password'])
        day_dict=dict()
        for i in range(day_num):
            day = datetime.datetime.now()+datetime.timedelta(days=-i)
            day_result=history_record(today=day,session=self.session,lottery=lottery,token=token,ssid1=ssid1,random=random_)
            day_dict[day.strftime("%Y-%m-%d")]=day_result
            print(day.strftime("%Y-%m-%d"))
        day_dict_keyslist=day_dict.keys()
        get_plan_info=self.get_plan()
        for day in list(day_dict_keyslist)[::-1]:
            print(day)
            投注总额=0
            累计输赢金额=0
            最高盈利金额=0
            最高亏损金额=0
            第一轮全挂次数=0
            全挂次数=0
            吃掉凶手=0
            bet_issue_list=day_dict[day].keys()
            for bet_issue in list(bet_issue_list)[::-1]:
                print(bet_issue)
                # self.set_issue(bet_issue)
                # self.set_result(day_dict[day][bet_issue]['result'])
                # 输赢判断
                game_profit = 0
                remove_location_index = []
                add_new_location = []
                for i, location in enumerate(self.location_list):
                    if location:
                        r = location.handle_result({
                            'issue': self.last_bet_issue,
                            'result': day_dict[day][bet_issue]['result']
                        },day=day)
                        if r:
                            game_profit += r['profit']
                            累计输赢金额+=r['profit']
                            if r['result'] == '赢':
                                remove_location_index.append(i)
                                win_back = self.get_win_back()
                                if win_back and (r['bet_times'] > 3) and (r['bet_times'] - win_back > 0):
                                #if (win_back and not r['p_id'] and r['bet_times'] >= win_back[0] and r['bet_times'] - win_back[1] > 0) or (win_back and r['p_id'] and r['bet_times'] - win_back[1] > 0):
                                    new_bet_times = r['bet_times'] - win_back
                                    new_out_index = None
                                    net_in_index = None
                                    cnt = 0
                                    for o_i, _1 in enumerate(r['amount']):
                                        for i_i, _2 in enumerate(_1):
                                            cnt += 1
                                            if cnt == new_bet_times:
                                                new_out_index = o_i
                                                net_in_index = i_i
                                                break
                                        if new_out_index:
                                            break
                                    self.location_created_id += 1
                                    add_new_location.append({
                                        'id': f'n{self.location_created_id}',
                                        'p_id': r['id'],
                                        'plan': r['plan'],
                                        'amount': r['amount'],
                                        'insert_item': self.insert_item,
                                        'set_item': self.set_item,
                                        'out_index': new_out_index,
                                        'in_index': net_in_index,
                                        'bet_times': new_bet_times
                                    })
                            elif r['result'] == '输':
                                if r['end']:
                                    remove_location_index.append(i)
                                    #self.set_out_end((1 + self.get_out_end()))
                                    全挂次数+=1
                                if r['out_index'] == 0 and r['in_lose']:
                                    #print('第一轮全爆')
                                    # self.set_one_out_end((1 + self.get_one_out_end()))
                                    第一轮全挂次数+=1

                            self.can_create_location = True
                if game_profit>0:
                    最高盈利金额=game_profit if game_profit>最高盈利金额 else 最高盈利金额
                else:
                    最高亏损金额=game_profit if game_profit<最高亏损金额 else 最高亏损金额

                remove_location_index.sort(reverse=True)
                for i in remove_location_index:
                    self.location_list.pop(i)

                for kw in add_new_location:
                    l = Location(**kw)
                    self.location_list.append(l)
                # self.set_lottery_profit((self.get_lottery_profit() + game_profit))
                self.last_bet_issue = ''
                # 止盈止损
                if self.get_lottery_profit() >= self.get_win_stop():
                    self.stop_running()
                    self.set_err_msg('止盈停止')
                    return
                elif (-1 * self.get_lottery_profit()) >= self.get_lose_stop():
                    self.stop_running()
                    self.set_err_msg('止损停止')
                    return

                # 创建location
                if self.can_create_location:
                    for p in get_plan_info:
                        self.location_created_id += 1
                        l = Location(id=f'n{self.location_created_id}',
                                    p_id='',
                                    plan=p,
                                    amount=self.get_amount(),
                                    insert_item=self.insert_item,
                                    set_item=self.set_item)
                        self.location_list.append(l)
                    self.can_create_location = False

                # 获取下一期的期号
                # bet_issue = getDownTimeAndQh(session=self.session)
                # bet_issue = period(session=self.session, lottery=lottery, token=token, ssid1=ssid1, random=random_)
                # if not bet_issue:
                #     return
                # self.set_next_issue(bet_issue['cpqh'])


                #balance = getHyje(session=self.session)
                # balance = account(session=self.session, token=token, ssid1=ssid1, random=random_)
                # if balance:
                #     self.set_balance(balance)

                # 组装下注数据
                # json = {
                #     'cpqh': bet_issue['cpqh'],
                #     'cpbm': 58,
                #     'category': 4,
                #     'rlist': []
                # }
                json = {
                    'bets': [],
                    'drawNumber': bet_issue,
                    'ignore': True,
                    'lottery': lottery,
                }

                remove_location_index = []
                for i, l in enumerate(self.location_list):
                    bet_params = l.get_bet_params(day_dict[day][bet_issue], bet_issue)
                    if bet_params == -1:
                        remove_location_index.append(i)
                    elif bet_params:
                        json['bets'] = json['bets'] + bet_params
                remove_location_index.sort(reverse=True)
                for i in remove_location_index:
                    self.location_list.pop(i)
                
                #print(json)
                if json['bets']:
                    for i in json['bets']:
                        投注总额+=i['amount']
                    for l in self.location_list:
                        l.confirm(issue=bet_issue)
                    self.last_bet_issue = bet_issue
                    # for l in self.location_list:
                    #     l.confirm(issue=bet_issue)
            write_month_excel(day,投注总额,累计输赢金额,最高盈利金额,最高亏损金额,第一轮全挂次数,全挂次数,吃掉凶手)


    def logic(self):
        # if time.time() - self.start_ts >= 3600:
        #         #     if self.get_account()['username'] and self.get_account()['password']:
        #         #         #if loginWzDf(session=self.session, account=self.get_account()['username'], password=self.get_account()['password']):
        #         #         if cashlogin(session=self.session, account=self.get_account()['username'], password=self.get_account()['password'], force_login=True):
        #         #             self.start_ts = time.time()
        #         #     else:
        #         #         #if loginGuest(session=self.session):
        #         #         if cashlogin(session=self.session, account=self.get_account()['username'], password=self.get_account()['password'], force_login=True):
        #         #             self.start_ts = time.time()

        ssid1="cafc972161ab0ded340b71b7b4a841e4"
        random_=""
        #token="4ffed063922e2c1a029533ada871dba82ce6b8a7"
        token = cashlogin(session=self.session, account=self.get_account()['username'], password=self.get_account()['password'])
        #lottery = 'XYFT'
        #open_result = findFjkjhmList(session=self.session)
        open_result = lastResult(session=self.session, lottery=lottery, token=token,ssid1=ssid1,random=random_)
        if not open_result:
            print(f'开奖结果接口没有数据 {open_result}')
            return

        if self.last_bet_issue and (self.last_bet_issue not in open_result):
            return

        if self.last_bet_issue:
            self.set_issue(self.last_bet_issue)
            self.set_result(open_result[self.last_bet_issue])
            print(f'开奖{self.last_bet_issue} {open_result[self.last_bet_issue]}')
            # 输赢判断
            game_profit = 0
            remove_location_index = []
            add_new_location = []
            for i, location in enumerate(self.location_list):
                if location:
                    r = location.handle_result({
                        'issue': self.last_bet_issue,
                        'result': open_result[self.last_bet_issue]
                    })
                    if r:
                        game_profit += r['profit']
                        if r['result'] == '赢':
                            remove_location_index.append(i)
                            win_back = self.get_win_back()
                            if win_back and (r['bet_times'] > 3) and (r['bet_times'] - win_back > 0):
                            #if (win_back and not r['p_id'] and r['bet_times'] >= win_back[0] and r['bet_times'] - win_back[1] > 0) or (win_back and r['p_id'] and r['bet_times'] - win_back[1] > 0):
                                new_bet_times = r['bet_times'] - win_back
                                new_out_index = None
                                net_in_index = None
                                cnt = 0
                                for o_i, _1 in enumerate(r['amount']):
                                    for i_i, _2 in enumerate(_1):
                                        cnt += 1
                                        if cnt == new_bet_times:
                                            new_out_index = o_i
                                            net_in_index = i_i
                                            break
                                    if new_out_index:
                                        break
                                self.location_created_id += 1
                                add_new_location.append({
                                    'id': f'n{self.location_created_id}',
                                    'p_id': r['id'],
                                    'plan': r['plan'],
                                    'amount': r['amount'],
                                    'insert_item': self.insert_item,
                                    'set_item': self.set_item,
                                    'out_index': new_out_index,
                                    'in_index': net_in_index,
                                    'bet_times': new_bet_times
                                })
                        elif r['result'] == '输':
                            if r['end']:
                                remove_location_index.append(i)
                                self.set_out_end((1 + self.get_out_end()))
                            if r['out_index'] == 0 and r['in_lose']:
                                print('第一轮全爆')
                                self.set_one_out_end((1 + self.get_one_out_end()))

                        self.can_create_location = True

            remove_location_index.sort(reverse=True)
            for i in remove_location_index:
                self.location_list.pop(i)

            for kw in add_new_location:
                l = Location(**kw)
                self.location_list.append(l)
            self.set_lottery_profit((self.get_lottery_profit() + game_profit))
            self.last_bet_issue = ''
            # 止盈止损
            if self.get_lottery_profit() >= self.get_win_stop():
                self.stop_running()
                self.set_err_msg('止盈停止')
                return
            elif (-1 * self.get_lottery_profit()) >= self.get_lose_stop():
                self.stop_running()
                self.set_err_msg('止损停止')
                return

        # 创建location
        if self.can_create_location:
            for p in self.get_plan():
                self.location_created_id += 1
                l = Location(id=f'n{self.location_created_id}',
                             p_id='',
                             plan=p,
                             amount=self.get_amount(),
                             insert_item=self.insert_item,
                             set_item=self.set_item)
                self.location_list.append(l)
            self.can_create_location = False

        # 获取下一期的期号
        # bet_issue = getDownTimeAndQh(session=self.session)
        bet_issue = period(session=self.session, lottery=lottery, token=token, ssid1=ssid1, random=random_)
        if not bet_issue:
            return
        self.set_next_issue(bet_issue['cpqh'])


        #balance = getHyje(session=self.session)
        balance = account(session=self.session, token=token, ssid1=ssid1, random=random_)
        if balance:
            self.set_balance(balance)

        # 组装下注数据
        # json = {
        #     'cpqh': bet_issue['cpqh'],
        #     'cpbm': 58,
        #     'category': 4,
        #     'rlist': []
        # }
        json = {
            'bets': [],
            'drawNumber': bet_issue['cpqh'],
            'ignore': True,
            'lottery': lottery,
        }

        remove_location_index = []
        for i, l in enumerate(self.location_list):
            bet_params = l.get_bet_params(open_result['last_result'], bet_issue['cpqh'])
            if bet_params == -1:
                remove_location_index.append(i)
            elif bet_params:
                json['bets'] = json['bets'] + bet_params
        remove_location_index.sort(reverse=True)
        for i in remove_location_index:
            self.location_list.pop(i)
        
        #print(json)
        if json['bets']:
            bet_r = bet(session=self.session, json_=json, token=token, ssid1=ssid1, random=random_)
            if bet_r:
            #if putLottery(session=self.session, json=json):
                self.last_bet_issue = bet_issue['cpqh']
                self.set_balance(bet_r['balance'])
                #5期一清空
                if bet_issue['cpqh']!='':
                    if int(bet_issue['cpqh'])%5==0:
                        self.delete_all_item()
                for l in self.location_list:
                    l.confirm(issue=bet_issue['cpqh'])
                self.insert_item(['', '', '', '', '', '', '', '', '', '', '', ''])
                sleep_time = (time.time() - (bet_issue['ndate'] / 1000))
                time.sleep(sleep_time if sleep_time > 0 else 0)