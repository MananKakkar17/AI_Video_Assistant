import yt_dlp
from pydub import AudioSegment
import glob
import os
import shutil

DOWNLOAD_DIR='downloaders'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_ffmpeg_dir() -> str | None:
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")
    if ffmpeg_path and ffprobe_path:
        bin_dir = os.path.dirname(ffmpeg_path)
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
        return bin_dir

    winget_pattern = os.path.join(
        os.environ.get("LOCALAPPDATA", ""),
        "Microsoft",
        "WinGet",
        "Packages",
        "Gyan.FFmpeg_*",
        "ffmpeg-*",
        "bin",
    )
    for bin_dir in glob.glob(winget_pattern):
        if (
            os.path.exists(os.path.join(bin_dir, "ffmpeg.exe"))
            and os.path.exists(os.path.join(bin_dir, "ffprobe.exe"))
        ):
            os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")
            AudioSegment.converter = os.path.join(bin_dir, "ffmpeg.exe")
            AudioSegment.ffmpeg = os.path.join(bin_dir, "ffmpeg.exe")
            AudioSegment.ffprobe = os.path.join(bin_dir, "ffprobe.exe")
            return bin_dir

    return None

def download_youtube_audio(url:str)->str:
    ffmpeg_dir = get_ffmpeg_dir()
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        ## supress all download progress logs in the terminal
    }
    if ffmpeg_dir:
        ydl_opts["ffmpeg_location"] = ffmpeg_dir

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace(".webm", ".wav").replace(".m4a", ".wav")
    return filename


## we have to use whisper ai thats why we are setting the audio to 16000 so it is compatable.
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    get_ffmpeg_dir()
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path



##converting audio into chunks
#slicing audio at every 10 min mark
def chunk_audio(wav_path:str,chunk_minutes:int=10)->list:
    audio=AudioSegment.from_wav(wav_path)
    chunk_ms=chunk_minutes*60 *1000

    chunks=[]

    for i,start in enumerate(range(0,len(audio),chunk_ms)):
        chunk=audio[start:start+chunk_ms]
        chunk_path=f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path,format="wav")

        chunks.append(chunk_path)

    return chunks
    
def process_input(source: str) -> list:
    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks
