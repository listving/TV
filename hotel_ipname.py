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
end_url = [] 
end_retu_url = ''
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

tonkiang_err = 0
foodieguide_err = 0
test_name = random.choice(diqu)
data = {
    'search': f'{test_name}'  # 使用f-string插入变量值（Python 3.6+）
}
for i in range(1, page + 1):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        if i == 1:
            url = 'http://foodieguide.com/iptvsearch/hoteliptv.php'
            print(url)
            response = requests.post(url, data=data, timeout=15)
        else:
            if len(end_retu_url) > 0:
                retu_url = end_retu_url.replace("?page=1", f'?page={i}')
            url = 'http://foodieguide.com/iptvsearch/hoteliptv.php' + retu_url
            print(url)
            response = requests.get(url, timeout=15)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            if i == 1:
                # 查找所有的<a>标签
                links = soup.find_all('a')
                
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
                                    end_retu_url = href
                                    print("更换参数名称，状态码：", response.status_code,seek_find)
                                    break
            if list_page == 0:
                # 查找具有指定class的div元素
                channel_div = soup.find('div', class_='channel')
                if channel_div:
                    # 获取div内的文本内容并去除首尾空白
                    text_content = channel_div.get_text(strip=True)
                    
                    # 尝试从文本内容中提取数字
                    match = re.search(r'\d+', text_content)
                    if match:
                        # 如果找到了数字，则提取并打印
                        number_str = match.group()
                        print('当前记录数：', number_str)
                        
                        # 计算总页数并打印
                        number = int(number_str)
                        list_page = number // 20 + 1
                        print('当前总页数：', list_page)
                    else:
                        # 如果没有找到数字，则打印提示信息
                        print('未能在文本内容中找到数字。')
                else:
                    # 如果没有找到具有指定class的div元素，则打印提示信息
                    print('未能找到具有指定class的div元素。')
    
            tables_div = soup.find("div", class_="tables")
            results = (
                tables_div.find_all("div", class_="result")
                if tables_div
                else []
            )
            if not any(
                result.find("div", class_="channel") for result in results
            ):
                #break
                print("Err-------------------------------------------------------------------------------------------------------")
            for result in results:
                # print("-------------------------------------------------------------------------------------------------------")
                # print(result)
                # print("-------------------------------------------------------------------------------------------------------")
                html_txt = f"{result}"
                if "暂时失效" not in html_txt:
                    m3u8_div = result.find("a")
                    if m3u8_div:
                        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+"  # 设置匹配的格式，如http://8.8.8.8:8888
                        urls_all = re.findall(pattern, m3u8_div.get('href'))
                        # print(urls_all)
                        if len(urls_all) > 0:
                            ip = urls_all[0]
                            italic_tags = result.find_all('i')
                            # 尝试获取第二个<i>标签
                            if len(italic_tags) >= 1:
                                # second_italic_tag = italic_tags[1]  # 索引从0开始，所以第二个标签的索引是1
                                for tag in italic_tags:
                                    if '上线' in tag.get_text():
                                        url_name = tag.get_text()
                                        break
                                    else:
                                        url_name = '未知'
                                name_html_txt = f"{url_name}"
                                name_html_txt = name_html_txt.replace(" ", "").replace("\n", "")
                                # print(name_html_txt)
                                # print("1===========================================================================================================")
                                if "移动" in html_txt:
                                    ipname = '移动'
                                elif "移通" in html_txt:
                                    ipname = '移动'
                                elif "视通" in html_txt:
                                    ipname = '广电'
                                elif "联通" in html_txt:
                                    ipname = '联通'
                                elif "电信" in html_txt:
                                    ipname = '电信'
                                else:
                                    ipname ='其他'
                                dq_name = contains_any_value(name_html_txt, diqu)
                                if ip not in not_ip:
                                    resultslist.append(f"{ipname},{ip},{dq_name}")
                                    print(f"{ipname},{ip},{dq_name}")
                                name_html_txt = ""
    except Exception as e:
        print(f"=========================>>> Thread {url} error {e}")
    finally:
        if list_page > 0:
            if i >= list_page:
                break
        
resultslist = set(resultslist)    # 去重得到唯一的URL列表

with open("iplist.txt", 'w', encoding='utf-8') as file:
    for iplist in resultslist:
        file.write(iplist + "\n")
        print(iplist)
    file.close()
sorted_list = sorted(resultslist)

def worker(thread_url,counter_id):
    try:
        # 创建一个Chrome WebDriver实例
        results = []
        #分离出运营商和IP
        in_name,in_url,dq_name = thread_url.split(',')
        chrome_options = Options()
        chrome_options.add_argument(f"user-data-dir=selenium{counter_id}")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_argument("blink-settings=imagesEnabled=false")
        driver = webdriver.Chrome(options=chrome_options)
        # 设置页面加载超时
        driver.set_page_load_timeout(60)  # 10秒后超时
     
        # 设置脚本执行超时
        driver.set_script_timeout(50)  # 5秒后超时
        # 使用WebDriver访问网页
        if is_odd_or_even(random.randint(1, 200)):
            page_url= f"http://tonkiang.us/hotellist.html?s={in_url}"
        else:
            page_url= f"http://foodieguide.com/iptvsearch/hotellist.html?s={in_url}"
        print(page_url)
        driver.get(page_url)  # 将网址替换为你要访问的网页地址
        WebDriverWait(driver, 45).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.tables")
                )
        )
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tables_div = soup.find("div", class_="tables")
        results = (
            tables_div.find_all("div", class_="result")
            if tables_div
            else []
        )
        if not any(
            result.find("div", class_="m3u8") for result in results
        ):
            #break
            print("Err-------------------------------------------------------------------------------------------------------")
        for result in results:
            #print(result)
            m3u8_div = result.find("div", class_="m3u8")
            url_int = m3u8_div.text.strip() if m3u8_div else None
            #取频道名称
            m3u8_name_div = result.find("div", class_="channel")
            url_name = m3u8_name_div.text.strip() if m3u8_div else None
            #－－－－－
            #print("-------------------------------------------------------------------------------------------------------")
            name =f"{url_name}"
            if len(name) == 0:
                name = "Err画中画"
            #print(name)
            urlsp =f"{url_int}"
            if len(urlsp) == 0:
                urlsp = "rtp://127.0.0.1"             
            # print(f"{dq_name}_{url_name}\t{url_int}")
            #print("-------------------------------------------------------------------------------------------------------")
            urlsp = urlsp.replace("http://67.211.73.118:9901", "")
            name = name.replace("cctv", "CCTV")
            name = name.replace("中央", "CCTV")
            name = name.replace("央视", "CCTV")
            name = name.replace("高清", "")
            name = name.replace("HD", "")
            name = name.replace("标清", "")
            name = name.replace("频道", "")
            name = name.replace("-", "")
            name = name.replace(" ", "")
            name = name.replace("PLUS", "+")
            name = name.replace("＋", "+")
            name = name.replace("(", "")
            name = name.replace(")", "")
            name = re.sub(r"CCTV(\d+)台", r"CCTV\1", name)
            name = name.replace("CCTV1综合", "CCTV1")
            name = name.replace("CCTV2财经", "CCTV2")
            name = name.replace("CCTV3综艺", "CCTV3")
            name = name.replace("CCTV4国际", "CCTV4")
            name = name.replace("CCTV4中文国际", "CCTV4")
            name = name.replace("CCTV4欧洲", "CCTV4")
            name = name.replace("CCTV5体育", "CCTV5")
            name = name.replace("CCTV6电影", "CCTV6")
            name = name.replace("CCTV7军事", "CCTV7")
            name = name.replace("CCTV7军农", "CCTV7")
            name = name.replace("CCTV7农业", "CCTV7")
            name = name.replace("CCTV7国防军事", "CCTV7")
            name = name.replace("CCTV8电视剧", "CCTV8")
            name = name.replace("CCTV9记录", "CCTV9")
            name = name.replace("CCTV9纪录", "CCTV9")
            name = name.replace("CCTV10科教", "CCTV10")
            name = name.replace("CCTV11戏曲", "CCTV11")
            name = name.replace("CCTV12社会与法", "CCTV12")
            name = name.replace("CCTV13新闻", "CCTV13")
            name = name.replace("CCTV新闻", "CCTV13")
            name = name.replace("CCTV14少儿", "CCTV14")
            name = name.replace("CCTV15音乐", "CCTV15")
            name = name.replace("CCTV16奥林匹克", "CCTV16")
            name = name.replace("CCTV17农业农村", "CCTV17")
            name = name.replace("CCTV17农业", "CCTV17")
            name = name.replace("CCTV5+体育赛视", "CCTV5+")
            name = name.replace("CCTV5+体育赛事", "CCTV5+")
            name = name.replace("CCTV5+体育", "CCTV5+")
            name = name.replace("CMIPTV", "")
            name = name.replace("内蒙卫视", "内蒙古卫视")
            name = name.replace("CCTVCCTV", "CCTV")
            if "http" in urlsp:
                # 获取锁
                lock.acquire()
                infoList.append(f"{dq_name}_{name}_{in_name},{urlsp}")
                # 释放锁
                lock.release()
        print(f"=========================>>> Thread {in_url} save ok")
    except Exception as e:
        print(f"=========================>>> Thread {in_url} caught an exception: {e}")
    finally:
        # 确保线程结束时关闭WebDriver实例
        driver.quit() 
        print(f"=========================>>> Thread {in_url}  quiting")
        # 标记任务完成
        time.sleep(0)

# 创建一个线程池，限制最大线程数为3
# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
#     # 提交任务到线程池，并传入参数
#     counter = increment_counter()
#     for i in sorted_list:  # 假设有5个任务需要执行
#         executor.submit(worker, i ,counter)

# 创建 ThreadPoolExecutor，但不立即启动
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

# 设置守护线程
for thread in executor._threads:
    thread.daemon = True

# 启动线程
with executor:
    counter = increment_counter()
    for i in sorted_list:
        executor.submit(worker, i, counter)


infoList = set(infoList)  # 去重得到唯一的URL列表
infoList = sorted(infoList)

with open("myitv.txt", 'w', encoding='utf-8') as file:
    for info in infoList:
        file.write(info + "\n")
        # print(info)
    file.close()
