import requests
import threading
live_urls = []
with open("cctv.txt", 'r', encoding='utf-8') as file:
    live_urls = file.readlines()
    file.close()
    
# 直播源检查回看的函数
def check_live_replay(live_url, timeout=5):  # 添加timeout参数，默认为5秒
    print(live_url)
    line = live_url.strip()
    count = line.count(',')
    if count == 1:
        if line:
            channel_name, a_url = line.split(',')
            api_url = a_url + '/api/check_replay'
            print(channel_name,api_url)
            try:
                # 发起请求并设置超时时间
                response = requests.get(api_url, timeout=timeout)
                
                # 检查响应状态码
                if response.status_code == 200:
                    # 解析返回的数据
                    data = response.json()
                    
                    # 假设返回的数据中有一个字段叫做 'replay_supported' 来表示是否支持回看
                    if data.get('replay_supported'):
                        print(f"直播源 {live_url} 支持回看。")
                    else:
                        print(f"直播源 {live_url} 不支持回看。")
                else:
                    print(f"请求失败，无法检查直播源 {live_url} 的回看功能。状态码: {response.status_code}")
            except requests.exceptions.Timeout:
                print(f"请求超时，无法检查直播源 {live_url} 的回看功能。")
            except requests.exceptions.RequestException as e:
                print(f"请求出错，无法检查直播源 {live_url} 的回看功能。错误信息: {e}")
        else:
            print(f"无效连接 {live_url} 。")
    else:
        print(f"无效连接 {live_url} 。")

# 并发检查回看的函数
def check_live_replays_concurrently(live_urls, num_threads, timeout=5):
    # 创建线程列表
    threads = []
    
    # 创建线程池
    for i in range(num_threads):
        # 线程的工作函数
        def worker(live_url):
            check_live_replay(live_url, timeout=timeout)
        
        # 创建线程，并将直播源URL作为参数传递
        t = threading.Thread(target=worker, args=(live_urls[i],))
        threads.append(t)
        t.start()
    
    # 等待所有线程完成
    for t in threads:
        t.join()

# 要使用的线程数量
num_threads = 10

# 超时时间（秒）
timeout = 5

# 并发检查回看功能
check_live_replays_concurrently(live_urls, num_threads, timeout)
