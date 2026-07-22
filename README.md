# YouTube Video Downloader
Download YouTube videos with full control over quality and format settings.

## Windows Users
**Method 1: Install FFmpeg via winget**
Important Windows Requirement: yt-dlp requires FFmpeg installed on your system to combine best video and audio streams (or convert to MP3). If you don't have it installed on Windows, you can install it easily using winget:

```bash
winget install FFmpeg
```

**Method 2: Install FFmpeg via Chocolatey (Easiest Alternative)**

```bash
choco install ffmpeg
```

**Method 3: Install FFmpeg via Scoop (Easiest Alternative)**

```bash
scoop install ffmpeg
```



## Quick Start

The simplest way to download a video:

```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

This downloads the video in best available quality as MP4 to DEFAULT DIRECTORY (OS_INSTALLATION/Download/YouTube)

## Options

### Quality Settings

Use `-q` or `--quality` to specify video quality:

- `best` (default): Highest quality available
- `1080p`: Full HD
- `720p`: HD
- `480p`: Standard definition
- `360p`: Lower quality
- `worst`: Lowest quality available

Example:
```bash
python scripts/download_video.py "URL" -q 720p
```

### Format Options

Use `-f` or `--format` to specify output format (video downloads only):

- `mp4` (default): Most compatible
- `webm`: Modern format
- `mkv`: Matroska container

Example:
```bash
python scripts/download_video.py "URL" -f webm
```

### Audio Only

Use `-a` or `--audio-only` to download only audio as MP3:

```bash
python scripts/download_video.py "URL" -a
```

### Custom Output Directory

Use `-o` or `--output` to specify a different output directory:

```bash
python scripts/download_video.py "URL" -o /path/to/directory
```

## Complete Examples

1. Download video in 1080p as MP4:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 1080p
```

2. Download audio only as MP3:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -a
```

3. Download in 720p as WebM to custom directory:
```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=VIDEO_ID" -q 720p -f webm -o /custom/path
```


## How It Works

A powerful YouTube downloader that

- Automatically installs itself if not present
- Retrieves video data prior to downloading
- Chooses the best streams that fit your requirements.
- When necessary, combines audio and video streams.
- Supports many different types of YouTube videos.

## Important Notes

- Downloads are automatically saved to ⁣`OS_INSTALLATION/Download/YouTube/`
- The video title automatically generates the video filename.
- The script automatically installs yt-dlp.
- Playlists are automatically skipped; only individual videos are downloaded.
- Higher quality videos might require more disk space and take longer to download.