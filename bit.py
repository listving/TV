import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stream_bitrate(url):
    # 将输出重定向到/dev/null（在Windows上使用NUL）
    null_device = '/dev/null' if os.name != 'nt' else 'NUL'
    cmd = f"ffmpeg -i {url} -hide_banner -loglevel error -f null - {null_device}"
    print(cmd)
    try:
        output = subprocess.check_output(cmd, shell=True, text=True)
        for line in output.splitlines():
            if "bitrate:" in line:
                bitrate = int(line.split()[1])
                return bitrate
    except subprocess.CalledProcessError as e:
        # 捕获并处理ffmpeg命令执行错误
        error_output = e.output
        error_returncode = e.returncode
        print(f"Error occurred while executing the command: {error_output}")
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
