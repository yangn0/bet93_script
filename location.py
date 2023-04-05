import copy
import os
import xlrd
import xlutils.copy
import xlwt
import time

import csv

key = {
    '1道1': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181301,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '1道2': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181302,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '1道3': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181303,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '1道4': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181304,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '1道5': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181305,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '1道6': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181306,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '1道7': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181307,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '1道8': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181308,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '1道9': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181309,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '1道10': {
        "pl": 9.8,
        "wflbbm": 4213,
        "wfbm3": 581181310,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '2道1': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181401,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '2道2': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181402,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '2道3': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181403,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '2道4': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181404,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '2道5': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181405,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '2道6': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181406,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '2道7': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181407,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '2道8': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181408,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '2道9': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181409,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '2道10': {
        "pl": 9.8,
        "wflbbm": 4214,
        "wfbm3": 581181410,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '3道1': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181501,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '3道2': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181502,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '3道3': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181503,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '3道4': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181504,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '3道5': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181505,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '3道6': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181506,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '3道7': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181507,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '3道8': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181508,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '3道9': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181509,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '3道10': {
        "pl": 9.8,
        "wflbbm": 4215,
        "wfbm3": 581181510,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '4道1': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181601,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '4道2': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181602,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '4道3': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181603,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '4道4': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181604,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '4道5': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181605,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '4道6': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181606,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '4道7': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181607,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '4道8': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181608,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '4道9': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181609,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '4道10': {
        "pl": 9.8,
        "wflbbm": 4216,
        "wfbm3": 581181610,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '5道1': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181701,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '5道2': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181702,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '5道3': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181703,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '5道4': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181704,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '5道5': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181705,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '5道6': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181706,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '5道7': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181707,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '5道8': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181708,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '5道9': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181709,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '5道10': {
        "pl": 9.8,
        "wflbbm": 4217,
        "wfbm3": 581181710,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '6道1': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181801,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '6道2': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181802,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '6道3': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181803,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '6道4': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181804,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '6道5': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181805,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '6道6': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181806,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '6道7': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181807,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '6道8': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181808,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '6道9': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181809,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '6道10': {
        "pl": 9.8,
        "wflbbm": 4418,
        "wfbm3": 581181810,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '7道1': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181901,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '7道2': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181902,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '7道3': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181903,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '7道4': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181904,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '7道5': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181905,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '7道6': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181906,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '7道7': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181907,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '7道8': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181908,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '7道9': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181909,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '7道10': {
        "pl": 9.8,
        "wflbbm": 4419,
        "wfbm3": 581181910,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '8道1': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182001,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '8道2': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182002,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '8道3': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182003,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '8道4': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182004,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '8道5': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182005,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '8道6': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182006,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '8道7': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182007,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '8道8': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182008,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '8道9': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182009,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '8道10': {
        "pl": 9.8,
        "wflbbm": 4420,
        "wfbm3": 581182010,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '9道1': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182101,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '9道2': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182102,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '9道3': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182103,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '9道4': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182104,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '9道5': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182105,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '9道6': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182106,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '9道7': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182107,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '9道8': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182108,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '9道9': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182109,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '9道10': {
        "pl": 9.8,
        "wflbbm": 4421,
        "wfbm3": 581182110,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    '10道1': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182201,
        "title": "1",
        "zs": 1,
        "price": 5
    },
    '10道2': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182202,
        "title": "2",
        "zs": 1,
        "price": 5
    },
    '10道3': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182203,
        "title": "3",
        "zs": 1,
        "price": 5
    },
    '10道4': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182204,
        "title": "4",
        "zs": 1,
        "price": 5
    },
    '10道5': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182205,
        "title": "5",
        "zs": 1,
        "price": 5
    },
    '10道6': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182206,
        "title": "6",
        "zs": 1,
        "price": 5
    },
    '10道7': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182207,
        "title": "7",
        "zs": 1,
        "price": 5
    },
    '10道8': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182208,
        "title": "8",
        "zs": 1,
        "price": 5
    },
    '10道9': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182209,
        "title": "9",
        "zs": 1,
        "price": 5
    },
    '10道10': {
        "pl": 9.8,
        "wflbbm": 4422,
        "wfbm3": 581182210,
        "title": "10",
        "zs": 1,
        "price": 5
    },
    # '1道大': {
    #     "pl": 2.1,
    #     "wflbbm": 4001,
    #     "wfbm3": 581180101,
    #     "title": "冠亚大",
    #     "zs": 1,
    #     "price": 5
    # },
    # '1道小': {
    #     "pl": 1.7,
    #     "wflbbm": 4001,
    #     "wfbm3": 581180102,
    #     "title": "冠亚小",
    #     "zs": 1,
    #     "price": 5
    # },
    # '1道单': {
    #     "pl": 1.7,
    #     "wflbbm": 4001,
    #     "wfbm3": 581180103,
    #     "title": "冠亚单",
    #     "zs": 1,
    #     "price": 5
    # },
    # '1道双': {
    #     "pl": 2.1,
    #     "wflbbm": 4001,
    #     "wfbm3": 581180104,
    #     "title": "冠亚双",
    #     "zs": 1,
    #     "price": 5
    # },

    '1道龙': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180201,
        "title": "龙",
        "zs": 1,
        "price": 5
    },
    '1道虎': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180202,
        "title": "虎",
        "zs": 1,
        "price": 5
    },
    '1道大': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180203,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '1道小': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180204,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '1道单': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180205,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '1道双': {
        "pl": 1.96,
        "wflbbm": 4002,
        "wfbm3": 581180206,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '2道龙': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180301,
        "title": "龙",
        "zs": 1,
        "price": 5
    },
    '2道虎': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180302,
        "title": "虎",
        "zs": 1,
        "price": 5
    },
    '2道大': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180303,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '2道小': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180304,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '2道单': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180305,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '2道双': {
        "pl": 1.96,
        "wflbbm": 4003,
        "wfbm3": 581180306,
        "title": "双",
        "zs": 1,
        "price": 5
    },
    '3道龙': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180401,
        "title": "龙",
        "zs": 1,
        "price": 5
    },
    '3道虎': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180402,
        "title": "虎",
        "zs": 1,
        "price": 5
    },
    '3道大': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180403,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '3道小': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180404,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '3道单': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180405,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '3道双': {
        "pl": 1.96,
        "wflbbm": 4004,
        "wfbm3": 581180406,
        "title": "双",
        "zs": 1,
        "price": 5
    },
    '4道龙': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180501,
        "title": "龙",
        "zs": 1,
        "price": 5
    },
    '4道虎': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180502,
        "title": "虎",
        "zs": 1,
        "price": 5
    },
    '4道大': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180503,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '4道小': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180504,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '4道单': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180505,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '4道双': {
        "pl": 1.96,
        "wflbbm": 4005,
        "wfbm3": 581180506,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '5道龙': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180601,
        "title": "龙",
        "zs": 1,
        "price": 5
    },
    '5道虎': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180602,
        "title": "虎",
        "zs": 1,
        "price": 5
    },
    '5道大': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180603,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '5道小': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180604,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '5道单': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180605,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '5道双': {
        "pl": 1.96,
        "wflbbm": 4006,
        "wfbm3": 581180606,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '6道大': {
        "pl": 1.96,
        "wflbbm": 4007,
        "wfbm3": 581180701,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '6道小': {
        "pl": 1.96,
        "wflbbm": 4007,
        "wfbm3": 581180702,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '6道单': {
        "pl": 1.96,
        "wflbbm": 4007,
        "wfbm3": 581180703,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '6道双': {
        "pl": 1.96,
        "wflbbm": 4007,
        "wfbm3": 581180704,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '7道大': {
        "pl": 1.96,
        "wflbbm": 4008,
        "wfbm3": 581180801,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '7道小': {
        "pl": 1.96,
        "wflbbm": 4008,
        "wfbm3": 581180802,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '7道单': {
        "pl": 1.96,
        "wflbbm": 4008,
        "wfbm3": 581180803,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '7道双': {
        "pl": 1.96,
        "wflbbm": 4008,
        "wfbm3": 581180804,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '8道大': {
        "pl": 1.96,
        "wflbbm": 4009,
        "wfbm3": 581180901,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '8道小': {
        "pl": 1.96,
        "wflbbm": 4009,
        "wfbm3": 581180902,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '8道单': {
        "pl": 1.96,
        "wflbbm": 4009,
        "wfbm3": 581180903,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '8道双': {
        "pl": 1.96,
        "wflbbm": 4009,
        "wfbm3": 581180904,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '9道大': {
        "pl": 1.96,
        "wflbbm": 4010,
        "wfbm3": 581181001,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '9道小': {
        "pl": 1.96,
        "wflbbm": 4010,
        "wfbm3": 581181002,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '9道单': {
        "pl": 1.96,
        "wflbbm": 4010,
        "wfbm3": 581181003,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '9道双': {
        "pl": 1.96,
        "wflbbm": 4010,
        "wfbm3": 581181004,
        "title": "双",
        "zs": 1,
        "price": 5
    },

    '10道大': {
        "pl": 1.96,
        "wflbbm": 4011,
        "wfbm3": 581181101,
        "title": "大",
        "zs": 1,
        "price": 5
    },
    '10道小': {
        "pl": 1.96,
        "wflbbm": 4011,
        "wfbm3": 581181102,
        "title": "小",
        "zs": 1,
        "price": 5
    },
    '10道单': {
        "pl": 1.96,
        "wflbbm": 4011,
        "wfbm3": 581181103,
        "title": "单",
        "zs": 1,
        "price": 5
    },
    '10道双': {
        "pl": 1.96,
        "wflbbm": 4011,
        "wfbm3": 581181104,
        "title": "双",
        "zs": 1,
        "price": 5
    }
}

# ['编号', '父编号', '计划', '中挂', '第几轮', '第几注', '期号', '开奖结果', '投注内容', '投注第几名',  '投注金额', '盈亏']


def write_2_excel(bh, fbh, zg, djl, djz, qh, kjjg, jh, tznr, tzdjm, tzje, yk, filename='bet_info.csv'):
    header = ["时间", '编号', '父编号', '中挂',   '第几轮', '第几注',
              '期号', '开奖结果', '计划', '投注内容', '投注第几名',  '投注金额', '盈亏']
    if filename in os.listdir('.'):
        # print("文件在")
        with open(filename, 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([time.strftime(
                '%Y/%m/%d %H:%M:%S'), bh, fbh, zg, djl, djz, qh, kjjg, jh, tznr, tzdjm, tzje, yk])
    else:
        with open(filename, 'a+', newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(header)
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow([time.strftime(
                '%Y/%m/%d %H:%M:%S'), bh, fbh, zg, djl, djz, qh, kjjg, jh, tznr, tzdjm, tzje, yk])

# ['编号', '父编号', '计划', '中挂', '第几轮', '第几注', '期号', '开奖结果', '投注内容', '投注第几名',  '投注金额', '盈亏']


def write_2_excel_1(bh, fbh, zg, djl, djz, qh, kjjg, jh, tznr, tzdjm, tzje, yk, filename='下注记录.xls'):
    if filename in os.listdir('.'):
        # print("文件在")
        data = xlrd.open_workbook(filename)
        sheet = data.sheet_by_index(0)
        row = sheet.nrows
        ws = xlutils.copy.copy(data)
        table = ws.get_sheet(0)
        table.write(row, 0, time.strftime('%Y/%m/%d %H:%M:%S'))
        table.write(row, 1, bh)
        table.write(row, 2, fbh)
        table.write(row, 3, zg)
        table.write(row, 4, djl)
        table.write(row, 5, djz)
        table.write(row, 6, qh)
        table.write(row, 7, kjjg)
        table.write(row, 8, jh)
        table.write(row, 9, tznr)
        table.write(row, 10, tzdjm)
        table.write(row, 11, tzje)
        table.write(row, 12, yk)
        ws.save(filename)
    else:
        # print("开始写入")
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet("data")
        worksheet.write(0, 0, label='时间')
        worksheet.write(0, 1, label='编号')
        worksheet.write(0, 2, label='父编号')
        worksheet.write(0, 3, label='中挂')
        worksheet.write(0, 4, label='第几轮')
        worksheet.write(0, 5, label='第几注')
        worksheet.write(0, 6, label='期号')
        worksheet.write(0, 7, label='开奖结果')
        worksheet.write(0, 8, label='计划')
        worksheet.write(0, 9, label='投注内容')
        worksheet.write(0, 10, label='投注第几名')
        worksheet.write(0, 11, label='投注金额')
        worksheet.write(0, 12, label='盈亏')

        worksheet.write(1, 0, label=time.strftime('%Y/%m/%d %H:%M:%S'))
        worksheet.write(1, 1, label=bh)
        worksheet.write(1, 2, label=fbh)
        worksheet.write(1, 3, label=zg)
        worksheet.write(1, 4, label=djl)
        worksheet.write(1, 5, label=djz)
        worksheet.write(1, 6, label=qh)
        worksheet.write(1, 7, label=kjjg)
        worksheet.write(1, 8, label=jh)
        worksheet.write(1, 9, label=tznr)
        worksheet.write(1, 10, label=tzdjm)
        worksheet.write(1, 11, label=tzje)
        worksheet.write(1, 12, label=yk)
        workbook.save(filename)


class Location:

    def __init__(self, id, p_id, plan, amount, insert_item, set_item, out_index=0, in_index=0, bet_times=1):
        self.id = id
        self.p_id = p_id
        self.plan = plan
        self.amount = amount
        self.insert_item = insert_item
        self.set_item = set_item

        self.item = None

        self.out_index = out_index  # 轮
        self.in_index = in_index   # 注
        self.bet_times = bet_times  # 总注

        self.change_bet_location = 0  # %3 == 0 的时候就换位置

        self.bet_issue = None
        self.bet_location = None  # 下注道
        self.bet_content = None  # 下注内容
        self.bet_params = None  # 下注参数
        self.bet_amount = None  # 下注金额
        self.bet_odd = None  # 下注赔率
        self.bet_confirm = False  # 下注确认

    def update_bet_result(self, result: str):
        # 更新输赢 返回一个具体要操作的内容
        into = {
            'out_index': self.out_index,
            'in_index': self.in_index,
            'bet_times': self.bet_times,
            'amount': self.amount,
            'result': result,
            'in_lose': False,  # 表示这轮结果全输了
            'end': False,       # 全爆了
            'id': self.id,
            'p_id': self.p_id,
            'plan': self.plan
        }
        if result == '赢':
            self.out_index = 0
            self.in_index = 0
            self.bet_times = 1

        elif result == '输':
            self.in_index += 1
            self.bet_times += 1
            if self.in_index >= len(self.amount[self.out_index]):
                # 这内轮已经爆啦
                into['in_lose'] = True

                # 外轮看下有没有爆
                self.out_index += 1
                if self.out_index >= len(self.amount):
                    # 外轮爆了
                    self.out_index = 0
                    self.in_index = 0
                    self.bet_times = 1
                    into['end'] = True
                else:
                    # 外轮没爆
                    self.in_index = 0
            else:
                # 内轮没有爆 不用处理
                pass
        self.change_bet_location += 1
        return into

    def get_amount(self) -> int:
        return self.amount[self.out_index][self.in_index]

    def get_bet_params(self, last_result: dict, bet_issue):
        if self.bet_confirm:
            return
        # if not self.p_id and int(bet_issue[-3:]) > 165 and self.out_index == 0:
        #     return -1
        print(f'id{self.id} out_index{self.out_index} in_index{self.in_index}')
        bet_params = []
        # if self.in_index == 0 or not self.bet_content:
        if (self.change_bet_location % len(self.amount[0]) == 0) or not self.bet_content:
            self.bet_location = last_result['result'].index(self.plan[0]) + 1
            for i in self.plan[1]:
                if i == '大' or i == '小':
                    single_p = {
                        'game': f'DX{self.bet_location}',
                        'contents': 'D' if i == '大' else 'X',
                        'amount': self.get_amount(),
                        'odds': 1.9999
                    }
                    bet_params.append(single_p)
                elif i == '单' or i == '双':
                    single_p = {
                        'game': f'DS{self.bet_location}',
                        'contents': 'D' if i == '单' else 'S',
                        'amount': self.get_amount(),
                        'odds': 1.9999
                    }
                    bet_params.append(single_p)
                else:
                    single_p = {
                        'game': f'B{self.bet_location}',
                        'contents': str(i),
                        'amount': self.get_amount(),
                        'odds': 9.99
                    }
                    bet_params.append(single_p)
                # p = copy.deepcopy(key[f'{self.bet_location}道{i}'])
                # p['price'] = self.get_amount()
                # bet_params.append(p)
            self.bet_content = self.plan[1]
            self.bet_params = bet_params
        else:
            for i in self.bet_params:
                i['amount'] = self.get_amount()
            bet_params = self.bet_params

        self.bet_amount = self.get_amount()
        self.bet_odd = bet_params[0]['odds']
        return bet_params

    def confirm(self, issue):
        if self.bet_confirm:
            return
        self.bet_issue = issue
        self.bet_confirm = True
        print(f'下注成功 编号{self.id} 父编号{self.p_id} 第几轮{self.out_index+1} in_index{self.in_index} 第几注{self.bet_times} 期号{issue} 投注内容{self.bet_content} 投注第几名{self.bet_location} 投注金额{self.bet_amount}')
        # ['编号', '父编号', '中挂', '第几轮', '第几注', '期号', '开奖结果', '计划', '投注内容', '投注第几名',  '投注金额', '盈亏']
        if self.bet_amount!=0:
            self.item = self.insert_item([self.id, self.p_id, '', f'{self.out_index+1}', f'{self.bet_times}', f'{issue}', '', f'{self.plan[0]}', f'{self.bet_content}', f'{self.bet_location}',  f'{(self.bet_amount*len(self.bet_content))}', ''])

    def check_win_lose(self, result: dict):

        if '大' in self.bet_content or '小' in self.bet_content:
            open_result = '大' if int(
                result['result'][self.bet_location-1]) > 5 else '小'
            if self.bet_content[0] == open_result:
                return '赢'
            else:
                return '输'
        elif '单' in self.bet_content or '双' in self.bet_content:
            open_result = '单' if int(
                result['result'][self.bet_location - 1]) % 2 == 1 else '双'
            if self.bet_content[0] == open_result:
                return '赢'
            else:
                return '输'
        else:
            open_result = result['result'][self.bet_location - 1]
            if open_result in self.bet_content:
                return '赢'
            else:
                return '输'

    def handle_result(self, result: dict):
        if not self.bet_confirm:
            print(f'check_win_lose  self.bet_confirm:{self.bet_confirm}')
            return
        if result['issue'] != self.bet_issue:
            print(f"check_win_lose {result['issue']} != {self.bet_issue}")
            return

        if self.check_win_lose(result=result) == '赢':
            profit = round(((self.bet_amount*self.bet_odd) -
                           (len(self.bet_content) * self.bet_amount)), 2)
            print(f'编号{self.id} 父编号{self.p_id} 中 第几轮{self.out_index+1} in_index{self.in_index} 第几注{self.bet_times} 期号{self.bet_issue} 投注内容{self.bet_content} 投注第几名{self.bet_location} 投注金额{self.bet_amount} 盈亏{profit}')
            # ['编号', '父编号', '中挂', '第几轮', '第几注', '期号', '开奖结果', '投注内容', '投注第几名', '投注金额', '盈亏']
            try:
                write_2_excel(bh=f'{self.id}', fbh=f'{self.p_id}', jh=f'{self.plan[0]}', zg='中', djl=f'{self.out_index+1}', djz=f'{self.bet_times}', qh=f'{self.bet_issue}',
                              kjjg=f'{result["result"]}', tznr=f'{self.bet_content}', tzdjm=f'{self.bet_location}', tzje=f'{(len(self.bet_content)*self.bet_amount)}', yk=f'{profit}')
            except:
                print("写入excel失败")
            info = self.update_bet_result('赢')
            info['profit'] = profit
            # self.set_item(item=self.item, column='中挂', value='中')
            # self.set_item(item=self.item, column='开奖结果', value=f'{result["result"]}')
            # self.set_item(item=self.item, column='盈亏', value=f'{profit}')
            self.bet_confirm = False
            return info
        else:
            profit = -1 * len(self.bet_content) * self.bet_amount
            print(f'编号{self.id} 父编号{self.p_id} 挂 第几轮{self.out_index+1} in_index{self.in_index} 第几注{self.bet_times} 期号{self.bet_issue} 投注内容{self.bet_content} 投注第几名{self.bet_location} 投注金额{self.bet_amount} 盈亏{profit}')
            # ['编号', '父编号', '中挂', '第几轮', '第几注', '期号', '开奖结果', '投注内容', '投注第几名', '投注金额', '盈亏']
            try:
                write_2_excel(bh=f'{self.id}', fbh=f'{self.p_id}', jh=f'{self.plan[0]}', zg='挂', djl=f'{self.out_index + 1}', djz=f'{self.bet_times}', qh=f'{self.bet_issue}',
                              kjjg=f'{result["result"]}', tznr=f'{self.bet_content}', tzdjm=f'{self.bet_location}', tzje=f'{(len(self.bet_content) * self.bet_amount)}', yk=f'{profit}')
            except:
                print("写入excel失败")
            info = self.update_bet_result('输')
            info['profit'] = profit
            # self.set_item(item=self.item, column='中挂', value='挂')
            # self.set_item(item=self.item, column='开奖结果', value=f'{result["result"]}')
            # self.set_item(item=self.item, column='盈亏', value=f'{profit}')
            self.bet_confirm = False
            return info
