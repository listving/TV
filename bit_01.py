import cv2
import threading

mport cv2
import logging
import io

def capture_logs(cap):
    # 创建一个日志处理器，将日志输出保存到变量中
    log_output = io.StringIO()
    log_handler = logging.StreamHandler(log_output)
    log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logging.getLogger('opencv4').addHandler(log_handler)
    logging.getLogger('opencv4').setLevel(logging.DEBUG)  # 设置日志级别

    # 执行您的操作
    ret, frame = cap.read()

    # 关闭日志处理器
    logging.getLogger('opencv4').removeHandler(log_handler)

    # 获取日志内容
    logs = log_output.getvalue()
    return logs, ret, frame

def is_stream_playable(url, timeout=5000):
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print(f"Error opening video stream or file: {url}")
        return False

    logs, ret, frame = capture_logs(cap)
    cap.release()

    if ret:
        print(logs)
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
        "http://14.117.233.245:9000/udp/239.253.43.46:5146"
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
