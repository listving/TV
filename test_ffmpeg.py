import subprocess
import re

# 流媒体的URL
# stream_url = 'http://14.19.199.43:8089/hls/28/index.m3u8'
stream_url = 'http://222.218.158.31:8181/tsfile/live/0005_1.m3u8'

# 使用ffprobe分析流媒体
ffprobe_command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name,width,height,bit_rate', '-of', 'default=noprint_wrappers=1:nokey=1', stream_url]

try:
    # 执行ffprobe命令并捕获输出
    ffprobe_output = subprocess.check_output(ffprobe_command, stderr=subprocess.STDOUT)
    print(ffprobe_output)
    # 使用正则表达式解析输出
    width_match = re.search(r'width=(\d+)', ffprobe_output.decode('utf-8'))
    height_match = re.search(r'height=(\d+)', ffprobe_output.decode('utf-8'))
    r_frame_rate_match = re.search(r'r_frame_rate=(\d+/\d+)', ffprobe_output.decode('utf-8'))
    codec_name_match = re.search(r'codec_name=(.+)', ffprobe_output.decode('utf-8'))
    
    # 提取并输出视频质量信息
    info = {
        'width': width_match.group(1) if width_match else 'N/A',
        'height': height_match.group(1) if height_match else 'N/A',
        'r_frame_rate': r_frame_rate_match.group(1) if r_frame_rate_match else 'N/A',
        'codec_name': codec_name_match.group(1) if codec_name_match else 'N/A'
    }
    
    print(f"分辨率: {info['width']}x{info['height']}")
    print(f"帧率: {info['r_frame_rate']}")
    print(f"编码格式: {info['codec_name']}")
    
except subprocess.CalledProcessError as e:
    # 如果ffprobe命令执行失败，输出错误信息
    print(f"无法分析流媒体: {e.output.decode('utf-8')}")

except Exception as e:
    # 捕获其他异常
    print(f"发生异常: {str(e)}")
