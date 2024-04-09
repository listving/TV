import subprocess

def check_video_source_with_ffmpeg(url):
    # 提取分辨率和码率
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout
        lines = output.split('\n')
        for line in lines:
            if 'codec_name' in line:
                codec_name = line.split('=')[1].strip()
            elif 'width' in line:
                width = int(line.split('=')[1].strip())
            elif 'height' in line:
                height = int(line.split('=')[1].strip())
            elif 'bit_rate' in line:
                bit_rate = int(line.split('=')[1].strip())
        
        return codec_name, width, height, bit_rate
    except subprocess.CalledProcessError:
        return None
    except subprocess.TimeoutExpired:
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
        
