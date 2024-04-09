import subprocess
import re

# 直播流的URL
stream_url = 'http://14.19.199.43:8089/hls/28/index.m3u8'

# ffprobe命令，用于获取直播流的详细信息
ffprobe_command = ['ffprobe', '-v', 'error', '-show_streams', '-of', 'default=noprint_wrappers=1:nokey=1', stream_url]

# 执行ffprobe命令，并捕获其输出
process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
output, _ = process.communicate()

# 将输出解码为字符串
output_str = output.decode('utf-8')

# 正则表达式，用于匹配码率信息
bitrate_pattern = re.compile(r'bitrate=\s*([0-9]+)')

# 初始化码率变量
bitrate = None

# 读取并解析ffprobe的输出
for line in output_str.split('\n'):
    match = bitrate_pattern.search(line)
    if match:
        # 找到码率信息，提取并转换为整数
        bitrate int =(match.group(1))
        print("当前码率为：")
        print(bitrate)
        break
    else:
        print("无法判断当前播放码率")
