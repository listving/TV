import subprocess

def check_live_stream(stream_url):
    # FFmpeg命令，尝试以最低延迟捕获直播流的前几帧
    # -probesize和-analyzeduration选项用于快速分析流
    # -ss 00:00:02表示尝试从流中捕获前2秒的数据
    # -f null表示不输出到文件，而是输出到stdout或stderr
    # -v error表示只输出错误信息
    ffmpeg_command = [
        'ffmpeg',
        '-probesize', '20M',
        '-analyzeduration', '20M',
        '-i', stream_url,
        '-ss', '00:00:10',
        '-f', 'null',
        '-v', 'error'
    ]

    try:
        # 运行FFmpeg命令并捕获输出
        completed_process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        
        # 检查命令的退出码。如果为0，表示成功。否则，表示出错。
        if completed_process.returncode == 0:
            print("直播源可以正常播放。")
        else:
            # 如果FFmpeg输出错误信息，打印出来
            error_output = completed_process.stderr.decode('utf-8')
            if error_output:
                print("直播源可能存在问题或加密:")
                print(error_output)
            else:
                print("无法确定直播源状态。")

    except Exception as e:
        # 如果发生其他异常（如网络问题、命令不存在等），也打印出来
        print(f"发生错误: {e}")

# 使用你的直播源URL替换这里的stream_url
stream_url = 'http://223.10.34.224:8083/udp/239.1.1.16:8016'
check_live_stream(stream_url)
