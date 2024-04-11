import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stream_bitrate(url):
    cmd = f"ffmpeg -i {url} -hide_banner -loglevel panic -streams_info"
    try:
        # 使用subprocess.run()来执行命令，并捕获标准输出和标准错误输出
        completed_process = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 检查命令是否成功执行
        if completed_process.returncode != 0:
            # 如果命令执行失败，从stderr中获取错误信息
            error_message = completed_process.stderr
            print(f"Error occurred while executing the command: {error_message}")
            return None
        
        # 如果命令执行成功，从stdout中获取比特率信息
        for line in completed_process.stdout.splitlines():
            if "bitrate:" in line:
                bitrate = int(line.split()[1])
                return bitrate
    except Exception as e:
        # 捕获其他可能发生的异常
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    urls = [
        "http://120.224.7.90:809/hls/204/index.m3u8",
    ]
    max_threads = 2

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(get_stream_bitrate, url): url for url in urls}

        for future in as_completed(futures):
            url = futures[future]
            try:
                bitrate = future.result()
                print(f"直播源码率（{url}）： {bitrate} bps")
            except Exception as e:
                print(f"获取码率失败（{url}）： {e}")

if __name__ == "__main__":
    main()
