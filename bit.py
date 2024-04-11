import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stream_bitrate(url):
    cmd = f"ffmpeg -i {url} -hide_banner -loglevel error"
    output = subprocess.check_output(cmd, shell=True, text=True)
    for line in output.splitlines():
        if "bitrate:" in line:
            bitrate = int(line.split()[1])
            return bitrate

def main():
    urls = [
        "http://124.230.56.143:55555/udp/239.76.253.151:9000",
        "http://219.159.194.195:8181/tsfile/live/0002_1.m3u8",
        "http://113.15.187.233:8181/tsfile/live/0016_1.m3u8",
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
