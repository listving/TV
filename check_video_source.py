import subprocess

def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
           '-show_entries', 'stream=codec_name,width,height,bit_rate', '-of',
           'default=noprint_wrappers=1:nokey=1', url]
    
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, timeout=10, text=True)
        output = result.stdout
        
        if output:
            # 解析输出并提取所需信息
            lines = output.split('\n')
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
        else:
            raise ValueError("ffprobe output was empty.")
    
    except subprocess.CalledProcessError as e:
        return f"ffprobe command failed with error: {e}"
    except subprocess.TimeoutExpired:
        return "ffprobe command timed out."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# 使用函数
try:
    video_url = 'http://59.55.35.219:20000/hls/1/index.m3u8'  # 替换成你的视频URL
    codec_name, width, height, bit_rate = check_video_source_with_ffmpeg(video_url)
    print(f"Video source information: Codec={codec_name}, Width={width}, Height={height}, Bit Rate={bit_rate}")
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")



        
