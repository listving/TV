import random
import concurrent.futures
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from bs4 import BeautifulSoup
from queue import Queue
import threading
import urllib.parse
import math
import requests
from requests.exceptions import Timeout

not_ip = [
    "14.19.199.43:8089",
]
lock = threading.Lock()

diqu = [
    "深圳",
    "广州",
    "揭阳",
    "汕头",
    "音乐",
    "经济",
    "文旅",
    "新闻",
    "综合",
    "cctv",
    "凤凰",
    "广西",
    "内蒙",
    "西藏",
    "天津",
    "北京",
    "重庆",
    "江苏",
    "香港",
    "青海",
    "甘肃",
    "陕西",
    "云南",
    "贵州",
    "四川",
    "海南",
    "广东",
    "湖南",
    "湖北",
    "河南",
    "山东",
    "江西",
    "福建",
    "安徽",
    "浙江",
    "黑龙江",
    "吉林",
    "辽宁",
    "山西",
    "河北",
    "上海"
    ]
random_choice = urllib.parse.quote(random.choice(diqu), safe='')
huabei = "北京市、天津市、河北省、山西省"
dongbei = "黑龙江省、吉林省、辽宁省、内蒙古自治区"
huadong = "上海市、江苏省、浙江省、安徽省、江西省、山东省、福建省、台湾省"
huazhong = "河南省、湖北省、湖南省"
huanan = "广东省、广西壮族自治区、海南省、香港特别行政区、澳门特别行政区"
xinan = "重庆市、四川省、贵州省、云南省、西藏自治区"
xibei = "陕西省、甘肃省、青海省、宁夏回族自治区、新疆维吾尔自治区、内蒙古自治区西部（阿拉善盟、巴彦淖尔市、乌海市、鄂尔多斯市）"

def contains_any_value(text, diqu):
    for dq in diqu:
        if dq in text:
            if dq in huabei:
                return dq+"_华北"
            elif dq in dongbei:
                return dq+"_东北"
            elif dq in huadong:
                return dq+"_华东"
            elif dq in huazhong:
                return dq+"_华中"
            elif dq in huanan:
                return dq+"_华南"  
            elif dq in xinan:
                return dq+"_西南"
            elif dq in xibei:
                return dq+"_西北"
            else:
                return dq+"_未知"
    return "未分类"
# 查找所有符合指定格式的网址
dqlist = []
infoList = []
urls_y = []
resultslist = []
page = random.randint(20, 40)
list_page = 0
seek_find = "rnd"
urls = [
    "http://tonkiang.us/hoteliptv.php?page=1&s=江苏",
    ]
# 初始化计数器为0
counter = -1
 
# 每次调用该函数时将计数器加1并返回结果
def increment_counter():
    global counter
    counter += 1
    return counter

#判断一个数字是单数还是双数可
def is_odd_or_even(number):
    if number % 2 == 0:
        return True
    else:
        return False

# 测试网站参数
end_url = []
test_url = 'http://foodieguide.com/iptvsearch/hoteliptv.php'  # 请替换为实际的提交URL
test_name = random.choice(diqu)
data = {
    'search': f'{test_name}'  # 使用f-string插入变量值（Python 3.6+）
}
print('测试url=',test_url)
response = requests.post(test_url, data=data)
response = requests.post(test_url, data=data)
if response.status_code == 200:
    try:
        print("请求成功，状态码：", response.status_code, test_name)
        # 打印响应内容
        html = response.text
        
        soup11 = BeautifulSoup(html, 'html.parser')
        print(soup11)
        # 查找所有的<a>标签
        links = soup11.find_all('a')
        print("***********************************************************************************")
        print(links)
        # 遍历所有的<a>标签，提取href属性，并解析出rnd的值
        for link in links:
            href = link.get('href')  # 获取href属性的值
            if href and 'page=' in href:
                print(href)  # 打印rnd的值
                count = href.count('&')
                print(count)
                if count >= 1:
                    bb = href.split('&')[1]
                    cou = bb.count('=')
                    if cou >= 1:
                        cc = bb.split('=')[0]
                        if len(cc) > 0:
                            seek_find = cc
                            end_url = href.split('&')
                            print("更换参数名称，状态码：", response.status_code,seek_find)
                            print(end_url)
                            break

    except Exception as e:
        print(f"=========================>>> error {e}")
print("***********************************************************************************")
