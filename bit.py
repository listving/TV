import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stream_bitrate(url):
    cmd = f"ffmpeg -i {url} -hide_banner -videoc h265 -loglevel error"
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.PIPE, shell=True, text=True)
        return 99
        # for line in output.splitlines():
        #     if "bitrate:" in line:
        #         bitrate = int(line.split()[1])
        #         return bitrate
    except subprocess.CalledProcessError as e:
        # 如果ffmpeg命令失败，捕获异常并提取错误信息
        error_output = e.stderr
        print(error_output)
        error_returncode = e.returncode
        print(f"Error occurred while executing the command: {error_output}")
        # 这里你可以选择如何处理错误，比如返回None或者抛出自定义的异常
        if "error while decoding MB" in error_output:
            return -1
        else:
            return 88

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
