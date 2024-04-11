import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_stream_bitrate(url):
    cmd = f"ffmpeg -i {url} -hide_banner -loglevel error"
    print(cmd)
    output = subprocess.check_output(cmd, shell=True, text=True)
    for line in output.splitlines():
        if "bitrate:" in line:
            bitrate = int(line.split()[1])
            return bitrate

def main():
    urls = [
        "http://14.19.199.43:5555/udp/239.77.1.131:5146",

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
