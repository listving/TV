import cv2
import threading
import subprocess
import re
import os

def is_stream_playable(url, timeout=5000):
    # 使用 ffprobe 来检查视频流
    ffprobe_cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                   '-show_entries', 'stream=codec_name', url]
    
    # 运行 ffprobe 并捕获标准错误输出
    try:
        ffprobe_process = subprocess.run(ffprobe_cmd, stderr=subprocess.PIPE, timeout=timeout)
        error_output = ffprobe_process.stderr.decode('utf-8')
    except subprocess.TimeoutExpired:
        error_output = "ffprobe timeout expired"
    except Exception as e:
        error_output = str(e)

    # 检查是否有错误信息
    if "non-existing PPS" in error_output or "decode_slice_header error" in error_output or "no frame!" in error_output:
        return False
    
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    cap.release()

    if ret:
        return True
    else:
        return False
        
def check_stream(url):
    if is_stream_playable(url):
        print(url,"直播源可以正常播放")
    else:
        print(url,"直播源无法播放")

def main():
    urls = [
        "http://14.112.82.130:2222/udp/239.253.43.47:5146",
        "http://14.19.199.43:5555/udp/239.77.1.131:5146",
        "http://14.117.233.245:9000/udp/239.253.43.46:5146",
        "http://121.235.191.182:12999/hls/20/index.m3u8",
    ]  # 将urls变量更改为包含多个视频流URL的列表
    thread_count = 3

    threads = []
    for i in range(thread_count):
        t = threading.Thread(target=check_stream, args=(urls[i],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
