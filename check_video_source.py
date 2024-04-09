import subprocess

def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout
        
        # 清理输出，去除可能的重复行
        lines = [line for line in output.split('\n') if line]
        lines = [line for i, line in enumerate(lines) if line != lines[i-1]]  # 去除重复行
        
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
        
        if codec_name and width and height:
            return codec_name, width, height, bit_rate
        else:
            raise ValueError("Failed to extract all required information from ffprobe output.")
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

if __name__ == "__main__":
    video_url = 'http://59.55.35.219:20000/hls/1/index.m3u8'  # 替换成你的视频URL
    try:
        codec_name, width, height, bit_rate = check_video_source_with_ffmpeg(video_url)
        if codec_name and width and height:
            print(f"Video source seems to be available. Codec: {codec_name}, Resolution: {width}x{height}, Bit Rate: {bit_rate} bps")
        else:
            print("There is an issue with the video source.")
    except ValueError as e:
        print(f"An error occurred while parsing ffprobe output: {e}")

        
