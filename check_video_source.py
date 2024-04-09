import subprocess
def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'codec_name,width,height,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout
        print("ffprobe output:")
        print(output)  # 打印 ffprobe 的输出以进行调试
        
        lines = output.split('\n')
        print("－－－－－－－－－－－－－－－－－－－－－－－－")
        lines = set(lines)
        print(lines)
        codec_name = None
        width = None
        height = None
        bit_rate = None
        
        for line in lines:
            if 'codec_name' in line:
                codec_name = line.split('=')[1].strip()
            elif 'width' in line:
                width = int(line.split('=')[1].strip())
            elif 'height' in line:
                height = int(line.split('=')[1].strip())
            elif 'bit_rate' in line:
                bit_rate = int(line.split('=')[1].strip())
        
        if codec_name is None or width is None or height is None or bit_rate is None:
            raise ValueError("Failed to extract all required information from ffprobe output.")
        
        return codec_name, width, height, bit_rate
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as e:
        print(f"An error occurred while parsing ffprobe output: {e}")
        return None

if __name__ == "__main__":
    video_url = 'http://59.55.35.219:20000/hls/1/index.m3u8'  # 替换成你的视频URL
    result = check_video_source_with_ffmpeg(video_url)
    if result:
        codec_name, width, height, bit_rate = result
        print(f"Video source seems to be available.")
        print(f"Codec Name: {codec_name}")
        print(f"Resolution: {width}x{height}")
        print(f"Bit Rate: {bit_rate} bps")
    else:
        print("There is an issue with the video source.")
        
