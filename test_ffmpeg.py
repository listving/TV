import subprocess
import re

# 直播流的URL
stream_url = 'http://223.10.34.224:8083/udp/239.1.1.16:8016'

# ffmpeg命令，用于获取直播流的详细信息
ffmpeg_command = ['ffmpeg', '-i', stream_url, '-c', 'copy', '-f', 'null', '-']

# 设置超时时间（例如：10秒）
timeout = 30

try:
    # 执行ffmpeg命令，并捕获其输出
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    # 正则表达式，用于匹配码率信息
    bitrate_pattern = re.compile(r'bitrate=\s*(\d+)kbits/s')
    
    # 初始化码率变量
    bitrate = None
    
    # 读取ffmpeg的输出，设置超时
    stdout, stderr = process.communicate(timeout=timeout)
    
    # 将输出按行分割并检查每一行
    for line in stdout.decode('utf-8').split('\n'):
        # 使用正则表达式搜索码率
        match = bitrate_pattern.search(line)
        if match:
            # 找到码率信息，提取并转换为整数
            bitrate = int(match.group(1))
            break

    # 输出码率
    if bitrate:
        print(f'直播流的码率是: {bitrate} kbps')
    else:
        print('无法获取直播流的码率')

except subprocess.TimeoutExpired:
    print('ffmpeg进程超时，未能获取码率信息')
    # 终止ffmpeg进程
    process.kill()
