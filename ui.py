from looper import Looper
from tkinter import *
from tkinter import ttk
import json
import threading
import time
import os
from functools import partial
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 屏蔽告警信息


# from location import Location
# from looper import Looper
# from api import userInfo, home_LoginOrRegister_login
#
#
#
#
# import time
# import sys

# def Beijing_time():
#     r=requests.get('https://www.baidu.com')
#     t=time.strptime(r.headers['date'],'%a, %d %b %Y %H:%M:%S GMT')
#     return time.mktime(t)+28800

# if(Beijing_time()-1672132694>=86400*2):
#     input("测试期已过，请联系作者。")
#     sys.exit()

keymap = {
    '极速飞艇': 'LUCKYSB',
    '极速赛车': 'PK10JSC',
    '澳洲幸运10': 'AULUCKY10',
    '幸运飞艇': 'XYFT',
    'SG飞艇': 'SGFT',
}


class UI:

    def __init__(self):
        self.looper = None
        self.location_list = [None, None, None, None, None,
                              None, None, None, None, None]
        self.var_amount_list = []
        self.var_start_list = []
        self.bulid_ui()

        self.session = requests.Session()
        self.rank_data = None
        self.lottery_name = None

        self.tk.mainloop()

    def bulid_ui(self):
        config = self.read_config()

        self.tk = Tk()
        self.tk.title('')
        self.tk.geometry('1300x650')

        self.var_run = StringVar()
        self.var_run.set('运行')
        Button(self.tk, textvariable=self.var_run, command=self.run).place(
            relx=0.1, rely=0.02, anchor=W)

        self.var_err_msg = StringVar()
        self.var_err_msg.set('err_msg')
        Label(self.tk, textvariable=self.var_err_msg, width=44,
              height=2).place(relx=0.15, rely=0.02, anchor=W)

        Label(self.tk, text='账号：', width=5, height=2).place(
            relx=0.01, rely=0.06, anchor=W)
        self.var_account = StringVar()
        self.var_account.set(config.get('var_account', ''))
        Entry(self.tk, textvariable=self.var_account, width=15).place(
            relx=0.04, rely=0.06, anchor=W)

        Label(self.tk, text='密码：', width=5, height=2).place(
            relx=0.01, rely=0.1, anchor=W)
        self.var_password = StringVar()
        self.var_password.set(config.get('var_password', ''))
        Entry(self.tk, textvariable=self.var_password, width=15,
              show='*').place(relx=0.04, rely=0.1, anchor=W)

        Label(self.tk, text='余额：', width=5, height=2).place(
            relx=0.02, rely=0.16, anchor=W)
        self.var_balance = DoubleVar()
        self.var_balance.set(0)
        Label(self.tk, textvariable=self.var_balance, width=7,
              height=2).place(relx=0.06, rely=0.16, anchor=W)

        Label(self.tk, text='盈亏：', width=5, height=2).place(
            relx=0.12, rely=0.16, anchor=W)
        self.var_lottery_profit = DoubleVar()
        self.var_lottery_profit.set(config.get('var_lottery_profit', 0))
        Entry(self.tk, textvariable=self.var_lottery_profit,
              width=8).place(relx=0.15, rely=0.16, anchor=W)

        Label(self.tk, text='第一轮全挂次数：', width=13, height=2).place(
            relx=0.02, rely=0.2, anchor=W)
        self.var_one_out_end = IntVar()
        self.var_one_out_end.set(config.get('var_one_out_end', 0))
        Entry(self.tk, textvariable=self.var_one_out_end,
              width=7).place(relx=0.11, rely=0.2, anchor=W)

        Label(self.tk, text='全挂次数：', width=13, height=2).place(
            relx=0.02, rely=0.25, anchor=W)
        self.var_out_end = IntVar()
        self.var_out_end.set(config.get('var_out_end', 0))
        Entry(self.tk, textvariable=self.var_out_end, width=7).place(
            relx=0.11, rely=0.25, anchor=W)

        Label(self.tk, text=f'金额：', width=5, height=2).place(
            relx=0.01, rely=0.3, anchor=W)
        self.var_money = StringVar()
        self.var_money.set(config.get(
            'var_money', '5-15-45#122-224-333#444-555-666'))
        Entry(self.tk, textvariable=self.var_money, width=35).place(
            relx=0.01, rely=0.33, anchor=W)

        Label(self.tk, text='中退几步：', width=15, height=2).place(
            relx=0.02, rely=0.39, anchor=W)
        self.var_win_back = IntVar()
        self.var_win_back.set(config.get('var_win_back', 2))
        Entry(self.tk, textvariable=self.var_win_back,
              width=7).place(relx=0.11, rely=0.39, anchor=W)

        Label(self.tk, text='止盈：', width=5, height=2).place(
            relx=0.02, rely=0.45, anchor=W)
        self.var_win_stop = IntVar()
        self.var_win_stop.set(config.get('var_win_stop', 9999))
        Entry(self.tk, textvariable=self.var_win_stop,
              width=7).place(relx=0.06, rely=0.45, anchor=W)

        Label(self.tk, text='止损：', width=5, height=2).place(
            relx=0.02, rely=0.5, anchor=W)
        self.var_lose_stop = IntVar()
        self.var_lose_stop.set(config.get('var_lose_stop', 3333))
        Entry(self.tk, textvariable=self.var_lose_stop,
              width=7).place(relx=0.06, rely=0.5, anchor=W)

        self.text_plan = Text(self.tk, width=11, height=20,
                              font=(None, 14, 'bold'))
        self.text_plan.place(relx=0.16, rely=0.68, anchor=W)
        self.text_plan.insert('end', config.get(
            'text_plan', '1#大\n2#双\n2#1-5-8\n3#双\n4#大'))

        # self.text_log = Text(self.tk, width=124, height=50)
        # #self.text_log.place(relx=0.36, rely=0.49, anchor=W)
        #
        # self.VScroll1 = Scrollbar(self.text_log, orient='vertical', command=self.text_log.yview)
        # #self.VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        # self.text_log.configure(yscrollcommand=self.VScroll1.set)

        self.var_issue = StringVar()
        self.var_issue.set('期号：000000001')
        Label(self.tk, textvariable=self.var_issue, width=24, height=2,
              font=(None, 13, 'bold')).place(relx=0.36, rely=0.03, anchor=W)

        self.var_result = StringVar()
        self.var_result.set('开奖：1,2,3,4,5,6,7,8,9,10')
        Label(self.tk, textvariable=self.var_result, width=25, height=2,
              font=(None, 13, 'bold')).place(relx=0.53, rely=0.03, anchor=W)

        self.var_next_issue = StringVar()
        self.var_next_issue.set('下期：000000002')
        Label(self.tk, textvariable=self.var_next_issue, width=25,
              height=2).place(relx=0.76, rely=0.03, anchor=W)

        columns = ['编号', '父编号', '中挂', '第几轮', '第几注', '期号',
                   '开奖结果', '计划', '投注内容', '投注第几名',  '投注金额', '盈亏']
        self.tv = ttk.Treeview(self.tk, columns=columns,
                               show='headings', height=29, padding=(1, 1, 1, 1))
        self.tv.place(relx=0.28, rely=0.52, anchor=W)

        self.tv.heading('编号', text='编号')
        self.tv.column('编号', width=45, anchor='nw')

        self.tv.heading('父编号', text='父编号')
        self.tv.column('父编号', width=45, anchor='nw')

        self.tv.heading('中挂', text='中挂')
        self.tv.column('中挂', width=50, anchor='nw')

        self.tv.heading('第几轮', text='第几轮')
        self.tv.column('第几轮', width=44, anchor='nw')

        self.tv.heading('第几注', text='第几注')
        self.tv.column('第几注', width=44, anchor='nw')

        self.tv.heading('期号', text='期号')
        self.tv.column('期号', width=105, anchor='nw')

        self.tv.heading('开奖结果', text='开奖结果')
        self.tv.column('开奖结果', width=215, anchor='nw')

        self.tv.heading('计划', text='计划')
        self.tv.column('计划', width=40, anchor='nw')

        self.tv.heading('投注内容', text='投注内容')
        self.tv.column('投注内容', width=150, anchor='nw')

        self.tv.heading('投注第几名', text='第几名')
        self.tv.column('投注第几名', width=44, anchor='nw')

        self.tv.heading('投注金额', text='金额')
        self.tv.column('投注金额', width=44, anchor='nw')

        self.tv.heading('盈亏', text='盈亏')
        self.tv.column('盈亏', width=100, anchor='nw')

        VScroll1 = Scrollbar(self.tv, orient='vertical', command=self.tv.yview)
        VScroll1.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        self.tv.configure(yscrollcommand=VScroll1.set)
        self.tv.tag_configure("evenColor", background="blue",
                              font=('', 0, 'bold'))  # 设置颜色

    def get_out_end(self):
        return self.var_out_end.get()

    def set_out_end(self, value):
        return self.var_out_end.set(value)

    def get_one_out_end(self):
        return self.var_one_out_end.get()

    def set_one_out_end(self, value):
        return self.var_one_out_end.set(value)

    def get_win_stop(self) -> int:
        return self.var_win_stop.get()

    def get_lose_stop(self) -> int:
        return self.var_lose_stop.get()

    def get_win_back(self) -> int:
        try:
            return self.var_win_back.get()
            # r = list(map(lambda i: int(i), self.var_win_back.get().strip().split('#')))
            # if len(r) != 2:
            #     return []
            # return r
        except:
            return 0

    def get_amount(self):
        return list(map(lambda i: list(map(lambda j: int(j), i.split('-'))), self.var_money.get().strip().split('#')))

    def get_plan(self):
        contents = self.text_plan.get(1.0, "end")
        # print(contents)
        contentList = contents.split('\n')
        plan = []
        try:
            for c in contentList:
                s = c.strip()
                if s:
                    v = s.split('#')
                    plan.append([v[0], v[1].split('-')])
            return plan
        except:
            return

    def set_err_msg(self, err_msg: str):
        self.var_err_msg.set(err_msg)

    def get_weburl(self):
        contents = self.text_weburl.get(1.0, "end")
        # print(contents)
        contentList = contents.split('\n')
        web_url = []
        try:
            for c in contentList:
                s = c.strip()
                if s:
                    web_url.append(s)
            return web_url
        except:
            return

    def set_issue(self, issue):
        self.var_issue.set(f'期号：{issue}')

    def set_result(self, result):
        self.var_result.set(f'开奖：{",".join(result)}')

    def set_close_second(self, close_second):
        while close_second > 0:
            self.var_close_second.set(f'距离封盘 {close_second}秒')
            time.sleep(1)
            close_second -= 1

    def set_next_issue(self, next_issue):
        self.var_next_issue.set(f'下一期：{next_issue}')

    def insert_items(self, data: list) -> list:
        items = []
        for i in data:
            if (data[4] == "8"):
                item = self.tv.insert('', 0, values=i, tags=("evenColor"))
            else:
                item = self.tv.insert('', 0, values=i)
            item = self.tv.insert('', 0, values=i)
            items.append(item)
        return items

    def insert_item(self, data):
        if (data[4] == "8"):
            item = self.tv.insert('', 0, values=data, tags=("evenColor"))
        else:
            item = self.tv.insert('', 0, values=data)
        return item

    def delete_all_item(self):
        self.tv.delete(*self.tv.get_children())

    def set_item(self, item, column, value):
        self.tv.set(item=item, column=column, value=value)

    def get_second_bet(self):
        return self.var_second_bet.get()

    def get_lottery(self) -> str:
        return keymap[self.cbx_lottery.get()]

    def get_account_password(self) -> list:
        return [self.var_account.get().strip(), self.var_password.get().strip()]

    def get_simulation(self):
        return self.var_simulation.get()

    def set_simulation(self, value: int):
        self.var_simulation.set(value=value)
        return value

    def set_balance(self, value: float) -> float:
        self.var_balance.set(round(value, 2))
        return value

    def get_balance(self) -> float:
        return self.var_balance.get()

    def set_profit(self, value: float) -> float:
        '''今日输赢'''
        self.var_profit.set(round(value, 2))
        return value

    def get_profit(self) -> float:
        '''今日输赢'''
        return self.var_profit.get()

    def set_lottery_profit(self, value: float) -> float:
        '''本程序统计的盈亏'''
        self.var_lottery_profit.set(round(float(value), 2))
        return value

    def get_lottery_profit(self) -> float:
        '''本程序统计的盈亏'''
        try:
            return float(self.var_lottery_profit.get())
        except:
            return 0

    def get_simulation_lose2real(self):
        return self.var_simulation_lose2real.get()

    def get_simulation_lose2real_value(self):
        return self.var_simulation_lose2real_value.get()

    def get_kill_bet_location(self):
        '''这里从1开始的注意'''

        contents = self.text_kill_bet_location.get(1.0, "end")
        # print(contents)
        contentList = contents.split('\n')
        kill_bet_location_list = []
        try:
            for c in contentList:
                s = c.strip()
                if s:
                    v = s.split('-')
                    kill_bet_location_list.append([int(v[0]), int(v[1])])
            return kill_bet_location_list
        except:
            return

    def get_money(self, index: int = -1):
        try:
            amounts = list(map(lambda item: int(item),
                           self.var_money.get().strip().split('-')))
            if index == -1:
                return amounts
            return amounts[index]
        except:
            return

    def get_alianchu(self):
        return self.var_alianchu.get()

    def get_blianchu(self):
        return self.var_blianchu.get()

    def get_ge_balance_notice(self):
        return self.var_ge_balance_notice.get()

    def get_le_balance_notice(self):
        return self.var_le_balance_notice.get()

    def refresh(self):
        self.show_account()

    def draw(self):
        account = self.get_account()
        password = self.get_password()
        if not account or not password:
            self.log(f'输入账号密码，才可以提现...')
        else:
            login_response = cashlogin(
                self.session, account=account, password=password)
            self.log(f'登陆 {login_response}')
            draw_response = draw(session=self.session, cardid=self.var_cardid.get(
            ), drawcode=self.var_drawcode.get(), drawamount=self.var_drawamount.get())
            self.log(f'提现 {draw_response}')
            self.show_account()
            self.write_config()

    def write_config(self):
        sava_json = {
            'var_account': self.var_account.get().strip(),
            'var_password': self.var_password.get().strip(),
            'var_lottery_profit': self.var_lottery_profit.get(),
            'var_one_out_end': self.var_one_out_end.get(),
            'var_money': self.var_money.get().strip(),
            'var_win_back': self.var_win_back.get(),
            'var_win_stop': self.var_win_stop.get(),
            'var_lose_stop': self.var_lose_stop.get(),
            'text_plan': self.text_plan.get(1.0, "end").strip(),
            'var_out_end': self.var_out_end.get()
        }
        with open('config.json', mode='w', encoding='utf-8') as file:
            file.write(json.dumps(sava_json))

    def read_config(self) -> dict:
        if not os.path.exists('config.json'):
            return dict()

        read_config = None
        with open('config.json', mode='r', encoding='utf-8') as file:
            read_config = json.loads(file.read())
        print(read_config)
        return read_config

    def log(self, info: str):
        # self.text_log.insert('end', f"{time.strftime('%Y/%m/%d %H:%M:%S')} - {info}\n")
        # self.text_log.see(END)
        print(f"{time.strftime('%Y/%m/%d %H:%M:%S')} - {info}\n")
        return info

    def get_password(self) -> str:
        return self.var_password.get()

    def get_odds(self) -> float:
        try:
            return float(self.var_odds.get())
        except:
            return 1.9999

    def get_profit_ge_stop(self) -> int:
        try:
            return self.var_profit_ge_stop.get()
        except:
            return 999999

    def get_start_time(self) -> list:
        if not self.var_start_time.get():
            return []
        try:
            return list(map(lambda item: int(item), self.var_start_time.get().split('#')))
        except:
            return []

    def get_start_location_index(self) -> list:
        if not self.var_start_location.get():
            return []
        try:
            return list(map(lambda item: int(item)-1, self.var_start_location.get().split('#')))
        except:
            return []

    def get_end_time(self) -> list:
        if not self.var_end_time.get():
            return []
        try:
            return list(map(lambda item: int(item), self.var_end_time.get().split('#')))
        except:
            return []

    def show_account(self):
        account_response = userInfo(self.session)
        if account_response:
            self.set_balance(value=account_response['balance'])
            self.set_profit(value=account_response['today_winlose'])

    def start_flag(self):
        if not self.looper:
            return
        if self.var_start.get() == '已暂停':
            self.looper.start_flag = True
            self.var_start.set('已启动')
        else:
            self.looper.start_flag = False
            self.var_start.set('已暂停')

    def get_account(self) -> dict:
        return {
            'username': self.var_account.get().strip(),
            'password': self.var_password.get().strip()
        }

    def run(self):
        self.write_config()

        if self.var_run.get() == '运行':
            if not self.looper:
                self.looper = Looper(
                    get_plan=self.get_plan,
                    get_amount=self.get_amount,
                    get_win_back=self.get_win_back,
                    get_account=self.get_account,
                    set_issue=self.set_issue,
                    set_result=self.set_result,
                    set_next_issue=self.set_next_issue,
                    get_lottery_profit=self.get_lottery_profit,
                    set_lottery_profit=self.set_lottery_profit,
                    stop_running=self.stop_running,
                    get_win_stop=self.get_win_stop,
                    get_lose_stop=self.get_lose_stop,
                    set_err_msg=self.set_err_msg,
                    get_one_out_end=self.get_one_out_end,
                    set_one_out_end=self.set_one_out_end,
                    set_balance=self.set_balance,
                    insert_item=self.insert_item,
                    delete_all_item=self.delete_all_item,
                    set_item=self.set_item,
                    write_config=self.write_config,
                    get_out_end=self.get_out_end,
                    set_out_end=self.set_out_end,

                )
            self.looper.flag = True
            self.var_run.set('正在运行')
        else:
            self.stop_running()

    def stop_running(self):
        self.looper.flag = False
        self.var_run.set('运行')

    def start_location(self, index: int):
        self.write_config()
        if self.var_start_list[index].get() == '启动':

            # if not self.rank_data or self.lottery_name != self.get_lottery():
            #     self.lottery_name = self.get_lottery()
            #     rank_data = gainrank(self.session, follow=self.get_follow(), lottery=self.lottery_name, m=self.get_m())
            #     if not rank_data:
            #         print('gainrank没拿到数据')
            #         return
            #     self.rank_data = rank_data
            #
            # eid = ''
            # for rank_location in self.rank_data['result']['list']:
            #     if rank_location['focus'].replace('f', '') == str(index+1):
            #         eid = rank_location['eid']
            #         break
            # if not eid:
            #     print('gainrank 没有eid')
            #     return

            location = Location(location_index=index,
                                eid=None,
                                get_amount=self.get_amount,
                                log=self.log,
                                session=self.session,
                                get_lottery=self.get_lottery,
                                get_odds=self.get_odds,
                                get_jiajian_num=self.get_jiajian_num,
                                get_alianchu=self.get_alianchu,
                                get_blianchu=self.get_blianchu)
            self.location_list[index] = location
            self.var_start_list[index].set('已启动..')
        else:
            self.stop_location(index)

    def stop_location(self, index: int):
        self.location_list[index] = None
        self.var_start_list[index].set('启动')


# 85。0。4183。83
if __name__ == "__main__":
    UI()
