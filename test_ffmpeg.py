import subprocess

# 流媒体的URL
stream_url = 'http://223.10.34.224:8083/udp/239.1.1.11:8011'

# FFmpeg命令，尝试打开流媒体并输出信息到stderr
ffmpeg_command = ['ffmpeg', '-i', stream_url, '-f', 'null', '-']

# 执行FFmpeg命令并捕获输出
try:
    process = subprocess.Popen(ffmpeg_command, stderr=subprocess.PIPE, universal_newlines=True)
    output, _ = process.communicate()
    
    # 检查FFmpeg输出中是否有错误信息
    if process.returncode != 0:
        # 如果返回码不为0，说明有错误发生
        error_message = output
        print(f"流媒体播放失败: {error_message.strip()}")
    else:
        # 如果没有错误信息，流媒体应该能够正常播放
        print("流媒体播放成功")
        
except Exception as e:
    # 捕获任何异常，可能是网络问题、FFmpeg错误等
    print(f"发生异常: {str(e)}")
