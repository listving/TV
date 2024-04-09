import subprocess
import re

def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,r_frame_rate,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]

    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout

        # 使用正则表达式匹配并提取信息
        pattern = r'^(codec_name=h264)\s+(width=(\d+))\s+(height=(\d+))\s+(r_frame_rate=(\d+/\d+))\s+(bit_rate=(\d+))'
        matches = re.findall(pattern, output, re.MULTILINE)

        if matches:
            # 假设我们只关心第一个匹配项（视频流）
            codec_name, width, height, frame_rate, bit_rate = matches[0]
            print(f"编码格式: {codec_name.split('=')[-1]}")
            print(f"分辨率: {width.split('=')[-1]}x{height.split('=')[-1]}")
            print(f"帧率: {frame_rate.split('=')[-1]}")
            print(f"比特率: {bit_rate.split('=')[-1]}")
            return codec_name.split('=')[-1], int(width.split('=')[-1]), int(height.split('=')[-1]), int(bit_rate.split('=')[-1]), frame_rate.split('=')[-1]
        else:
            print("未找到匹配的视频流信息。")
            return None

    except subprocess.CalledProcessError as e:
        return f"ffprobe command failed with error: {e}"
    except subprocess.TimeoutExpired:
        return "ffprobe command timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# 使用函数
try:
    video_url = 'http://14.19.199.43:8089/hls/28/index.m3u8'  # 替换成你的视频URL
    codec_name, width, height, bit_rate = check_video_source_with_ffmpeg(video_url)
    print(f"Video source information: Codec={codec_name}, Width={width}, Height={height}, Bit Rate={bit_rate}")
except ValueError as e:
    print(f"Error parsing ffprobe output: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
