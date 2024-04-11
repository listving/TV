import cv2
import sys
import concurrent.futures

def get_video_info(url, timeout):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        print("无法打开视频文件")
        sys.exit()

    # 获取分辨率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("分辨率： {}x{}".format(width, height))

    # 获取码率
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    bitrate = (frame_count * width * height * 3) / duration
    print("码率： {:.2f} Mbps".format(bitrate / 1000000))

    cap.release()
    return url, (width, height), bitrate

def main(urls, timeout, num_threads):
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(get_video_info, url, timeout) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result(timeout=timeout)
                print("视频地址：", result[0])
                print("分辨率： {}x{}".format(result[1][0], result[1][1]))
                print("码率： {:.2f} Mbps".format(result[2] / 1000000))
            except concurrent.futures.TimeoutError:
                print("任务超时")

if __name__ == "__main__":
    urls = [
        "http://14.112.82.130:2222/udp/239.253.43.47:5146",
        "http://14.19.199.43:5555/udp/239.77.1.131:5146",
    ]  # 将urls变量更改为包含多个视频流URL的列表
    timeout = 5  # 设置超时限制，单位为秒
    num_threads = 4  # 设置线程数量
    main(urls, timeout, num_threads)
