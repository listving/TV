import subprocess
import re

# 流媒体的URL
# stream_url = 'http://14.19.199.43:8089/hls/28/index.m3u8'
stream_url = 'http://222.218.158.31:8181/tsfile/live/0007_1.m3u8'
# 使用ffprobe分析流媒体
ffprobe_command = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate,codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', stream_url]

try:
    # 执行ffprobe命令并捕获输出
    ffprobe_output = subprocess.check_output(ffprobe_command, stderr=subprocess.STDOUT)
    print(ffprobe_output)
    # 分析输出以获取视频质量信息
    info = {}
    for line in ffprobe_output.decode('utf-8').split('\n'):
        key, value = line.split('=')
        info[key] = value

    # 输出视频质量信息
    print(f"分辨率: {info['width']}x{info['height']}")
    print(f"帧率: {info['r_frame_rate']}")
    print(f"编码格式: {info['codec_name']}")
    
except subprocess.CalledProcessError as e:
    # 如果ffprobe命令执行失败，输出错误信息
    print(f"无法分析流媒体: {e.output.decode('utf-8')}")

except Exception as e:
    # 捕获其他异常
    print(f"发生异常: {str(e)}")
