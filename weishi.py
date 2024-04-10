import subprocess
import concurrent.futures
import os
import re
import time
import datetime
import threading
from queue import Queue
import requests
import eventlet
eventlet.monkey_patch()

# 线程安全的队列，用于存储下载任务
task_queue = Queue()
lock = threading.Lock()
# 线程安全的列表，用于存储结果
results = []

channels = []
error_channels = []
headers={'User-Agent': 'okhttp/3.15 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
se=requests.Session()

with open("itv.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                name =(f"{channel_name}")
                name = name.replace("TVB3明珠", "香港明珠卫视")
                name = name.replace("明珠台", "香港明珠卫视")
                name = name.replace("TVB2翡翠", "TVB翡翠卫视")
                name = name.replace("星影", "星空卫视")
                name = name.replace("本港卫视台", "星空卫视")
                if '卫视' in channel_name:
                    channels.append((name, channel_url))
    file.close()
    
# 定义工作线程函数
def worker():
    while True:
        # 从队列中获取一个任务
        channel_name, channel_url = task_queue.get()
        if ".m3u8" in channel_url or ".flv" in channel_url or ".mp4" in channel_url:
            try:
                channel_url_t = channel_url.rstrip(channel_url.split('/')[-1])  # m3u8链接前缀
                lines = requests.get(channel_url,headers=headers, timeout=3, stream=True).text.strip().split('\n')  # 获取m3u8文件内容
                ts_lists = [line.split('/')[-1] for line in lines if line.startswith('#') == False]  # 获取m3u8文件下视频流后缀
                ts_lists_0 = ts_lists[0].rstrip(ts_lists[0].split('.ts')[-1])  # m3u8链接前缀
                ts_url = channel_url_t + ts_lists[0]  # 拼接单个视频片段下载链接
    
                # 多获取的视频数据进行5秒钟限制
                with eventlet.Timeout(5, False):
                    start_time = time.time()
                    content = requests.get(ts_url,headers=headers, timeout=(3,4), stream=True).content
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1
    
                if content:
                    with open(ts_lists_0, 'ab') as f:
                        f.write(content)  # 写入文件
                    file_size = len(content)
                    # print(f"文件大小：{file_size} 字节")
                    download_speed = file_size / response_time / 1024
                    # print(f"下载速度：{download_speed:.3f} kB/s")
                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)  # 将速率从kB/s转换为MB/s并限制在1~100之间
                    #print(f'{channel_url}')
                    #print(f"m3u8 标准化后的速率：{normalized_speed:.3f} MB/s")
    
                    # 删除下载的文件
                    os.remove(ts_lists_0)
                    result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                    # 获取锁
                    lock.acquire()
                    results.append(result)
                    # 释放锁
                    lock.release()
                    numberx = (len(results) + len(error_channels)) / len(channels) * 100
                    # print(f"可用频道：{len(results)} 个 , 不可用频道：{len(error_channels)} 个 , 总频道：{len(channels)} 个 ,总进度：{numberx:.2f} %。")
            except:
                error_channel = channel_name, channel_url
                # error_channels.append(error_channel)
                numberx = (len(results) + len(error_channels)) / len(channels) * 100
        else:
            try:
                now=time.time()
                chunk_size = 3145728
                res=se.get(channel_url,headers=headers,stream=True,timeout=5)
                if res.status_code==200:
                    total_received = 0
                    for k in res.iter_content(chunk_size=chunk_size):
                        # 这里的chunk_size是1MB，每次读取1MB测试视频流
                        # 如果能获取视频流，则输出读取的时间以及链接
                        if time.time()-now > 15:
                            res.close()
                            print(f'Time out\t{channel_url}')
                            break
                        else:
                            if k:
                                chunk_len = len(k)
                                if chunk_len >= chunk_size:
                                    print(f'{time.time()-now:.2f}\t{channel_url}')
                                    response_time = (time.time()-now) * 1
                                    download_speed = chunk_len / response_time / 1024
                                    normalized_speed = min(max(download_speed / 1024, 0.001), 100)
                                    if response_time > 2.8:
                                        result = channel_name, channel_url, f"{normalized_speed:.3f} MB/s"
                                        # 获取锁
                                        lock.acquire()
                                        results.append(result)
                                        # 释放锁
                                        lock.release()
                                    else:
                                        print(f'X\t{channel_url}')
                                    break
                                else:
                                    print(f'X 数据块小于设置值 \t{channel_url}')
            except:
                # 无法连接并超时的情况下输出“X”
                print(f'X\t{channel_url}')
        
        # 减少CPU占用
        time.sleep(0)
        # 标记任务完成
        task_queue.task_done()

# 创建多个工作线程
num_threads = 100
for _ in range(num_threads):
    t = threading.Thread(target=worker, daemon=True) 
    #t = threading.Thread(target=worker, args=(event,len(channels)))  # 将工作线程设置为守护线程
    t.start()
    #event.set()

# 添加下载任务到队列
for channel in channels:
    task_queue.put(channel)

# 等待所有任务完成
task_queue.join()
# 测试分辨率
def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,r_frame_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=20, text=True)
        output = result.stdout
        # print(output)
        # 使用正则表达式匹配并提取信息
        pattern = r'^(h264)\s+(\d+)\s+(\d+)\s+(\d+/\d+)?$'
        matches = re.findall(pattern, output, re.MULTILINE)
        
        if matches:
            codec_name, width, height, r_frame_rate = matches[0]
            return codec_name, int(width), int(height), int(eval(r_frame_rate))
        else:
            raise ValueError("No valid matches found in ffprobe output.")
    
    except subprocess.CalledProcessError as e:
        return f"ffprobe command failed with error: {e}"
    except subprocess.TimeoutExpired:
        return "ffprobe command timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_video(video_url):
    channel_name, channel_url, speed = video_url
    try:
        codec_name, width, height, r_frame_rate = check_video_source_with_ffmpeg(channel_url)
        return (codec_name, width, height, r_frame_rate)
    except ValueError as e:
        print(f"Error parsing ffprobe output for {video_url}: {e}")
        return (None, None, None, None)
    except Exception as e:
        print(f"An error occurred for {video_url}: {e}")
        return (None, None, None, None)

# 最大线程数
max_workers = 50
video_urls = set(results)
results = []
# 使用ThreadPoolExecutor创建线程池
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # 提交任务到线程池
    future_to_url = {executor.submit(process_video, url): url for url in video_urls}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            # 获取任务返回的结果（分辨率和码率）
            resolution_and_bitrate = future.result()
            # 处理或记录结果
            print(f"Results for {url}: {resolution_and_bitrate}")
            codec_name, width, height, r_frame_rate = resolution_and_bitrate
            if codec_name == 'h264' and width >= 720 and r_frame_rate < 50:
                results.append(url)
        except Exception as exc:
            print(f'{url} generated an exception: {exc}')
# 打开移动源文件
with open("chinamobile.txt", 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        count = line.count(',')
        if count == 1:
            if line:
                channel_name, channel_url = line.split(',')
                if '卫视' in channel_name:
                    result = channel_name, channel_url, "0.001 MB/s"
                    results.append(result)

def channel_key(channel_name):
    match = re.search(r'\d+', channel_name)
    if match:
        return int(match.group())
    else:
        return float('inf')  # 返回一个无穷大的数字作为关键字

# 对频道进行排序
results.sort(key=lambda x: (x[0], -float(x[2].split()[0])))
#results.sort(key=lambda x: channel_key(x[0]))
now_today = datetime.date.today()
# 将结果写入文件

result_counter = 15  # 每个频道需要的个数

with open("weishi.txt", 'w', encoding='utf-8') as file:
    channel_counters = {}
    file.write('【  卫视频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name and '高清' not in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1

    channel_counters = {}
    file.write('【  卫视高清频道  】,#genre#\n')
    for result in results:
        channel_name, channel_url, speed = result
        if '卫视' in channel_name and '高清' in channel_name:
            if channel_name in channel_counters:
                if channel_counters[channel_name] >= result_counter:
                    continue
                else:
                    file.write(f"{channel_name},{channel_url}\n")
                    channel_counters[channel_name] += 1
            else:
                file.write(f"{channel_name},{channel_url}\n")
                channel_counters[channel_name] = 1
    file.close()
