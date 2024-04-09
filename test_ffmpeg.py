import subprocess
import re

# 直播流的URL
stream_url = 'http://223.10.34.224:8083/udp/239.1.1.16:8016'

# ffmpeg命令，用于获取直播流的详细信息
ffmpeg_command = ['ffmpeg', '-i', stream_url, '-c', 'copy', '-f', 'null', '-']

# 执行ffmpeg命令，并捕获其输出
process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# 正则表达式，用于匹配码率信息
bitrate_pattern = re.compile(r'bitrate=\s*(\d+)kbits/s')

# 初始化码率变量
bitrate = None

# 读取ffmpeg的输出
for line in iter(process.stdout.readline, b''):
    # 将字节解码为字符串
    line = line.decode('utf-8')
    # 打印输出，可选
    print(line, end='')
    
    # 使用正则表达式搜索码率
    match = bitrate_pattern.search(line)
    if match:
        # 找到码率信息，提取并转换为整数
        bitrate = int(match.group(1))
        break

# 确保ffmpeg进程结束
process.communicate()

# 输出码率
if bitrate:
    print(f'直播流的码率是: {bitrate} kbps')
else:
    print('无法获取直播流的码率')
