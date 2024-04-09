import concurrent.futures
import subprocess
import re

def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout
        
        # 使用正则表达式匹配并提取信息
        pattern = r'^(h264)\s+(\d+)\s+(\d+)\s+(N/A)?$'
        matches = re.findall(pattern, output, re.MULTILINE)
        
        if matches:
            codec_name, width, height, bit_rate = matches[0]
            return codec_name, int(width), int(height), bit_rate if bit_rate else None
        else:
            raise ValueError("No valid matches found in ffprobe output.")
    
    except subprocess.CalledProcessError as e:
        return f"ffprobe command failed with error: {e}"
    except subprocess.TimeoutExpired:
        return "ffprobe command timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def process_video(video_url):
    try:
        codec_name, width, height, bit_rate = check_video_source_with_ffmpeg(video_url)
        return (codec_name, width, height, bit_rate)
    except ValueError as e:
        print(f"Error parsing ffprobe output for {video_url}: {e}")
        return (None, None, None, None)
    except Exception as e:
        print(f"An error occurred for {video_url}: {e}")
        return (None, None, None, None)

# 视频URL列表
video_urls = [
    'http://59.55.35.219:20000/hls/1/index.m3u8',  # 替换成你的视频URL
    'http://221.5.12.130:2223/hls/69/index.m3u8',
    'http://219.137.29.213:4433/tsfile/live/0002_1.m3u8',
    'http://1.193.57.68:8800/rtp/239.16.20.1:10010',
    'http://221.198.174.113:8888/udp/225.1.1.120:5002'
]

# 最大线程数
max_workers = 5

# 使用ThreadPoolExecutor创建线程池
results = []
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
            results.append(resolution_and_bitrate)
        except Exception as exc:
            print(f'{url} generated an exception: {exc}')




