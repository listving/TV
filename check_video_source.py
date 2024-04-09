# check_video_source.py
import subprocess

def check_video_source_with_ffmpeg(url):
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1', url]
    try:
        subprocess.run(cmd, check=True, timeout=10)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False

video_url = 'your_video_url_here'  # 这里应该是一个变量，而不是硬编码的URL
if __name__ == "__main__":
    if check_video_source_with_ffmpeg(video_url):
        print("Video source seems to be available.")
    else:
        print("There is an issue with the video source.")
