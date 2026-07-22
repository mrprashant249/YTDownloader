"""
YouTube Video Downloader
Downloads videos from YouTube with customizable quality and format options.
Cross-platform compatible (Windows, macOS, Linux).
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def get_default_download_dir():
    """Get the user's default Downloads directory on Windows, macOS, or Linux."""
    home = Path.home()
    downloads = home / "Downloads" / "YouTube"
    downloads.mkdir(parents=True, exist_ok=True)
    return str(downloads)


def check_yt_dlp():
    """Check if yt-dlp is installed, install if not."""
    try:
        # Check as a module via python -m yt_dlp
        subprocess.run([sys.executable, "-m", "yt_dlp", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("yt-dlp not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)


def get_video_info(url):
    """Get information about the video without downloading."""
    result = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--dump-json", "--no-playlist", url],
        capture_output=True,
        text=True,
        check=True
    )
    return json.loads(result.stdout)


def download_video(url, output_path=None, quality="best", format_type="mp4", audio_only=False):
    """
    Download a YouTube video.

    Args:
        url: YouTube video URL
        output_path: Directory to save the video
        quality: Quality setting (best, 1080p, 720p, 480p, 360p, worst)
        format_type: Output format (mp4, webm, mkv, etc.)
        audio_only: Download only audio (mp3)
    """
    check_yt_dlp()

    if not output_path:
        output_path = get_default_download_dir()

    # Ensure output directory exists on Windows/Linux
    out_dir = Path(output_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build template in a cross-platform safe way
    output_template = str(out_dir / "%(title)s.%(ext)s")

    # Build command using python -m yt_dlp
    cmd = [sys.executable, "-m", "yt_dlp"]

    if audio_only:
        cmd.extend([
            "-x",  # Extract audio
            "--audio-format", "mp3",
            "--audio-quality", "0",  # Best quality
        ])
    else:
        # Video quality settings
        if quality == "best":
            format_string = "bestvideo+bestaudio/best"
        elif quality == "worst":
            format_string = "worstvideo+worstaudio/worst"
        else:
            # Specific resolution (e.g., 1080p, 720p)
            height = quality.replace("p", "")
            format_string = f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"

        cmd.extend([
            "-f", format_string,
            "--merge-output-format", format_type,
        ])

    # Output template
    cmd.extend([
        "-o", output_template,
        "--no-playlist",  # Don't download playlists by default
    ])

    cmd.append(url)

    print(f"Downloading from: {url}")
    print(f"Quality: {quality}")
    print(f"Format: {'mp3 (audio only)' if audio_only else format_type}")
    print(f"Output Directory: {out_dir.resolve()}\n")

    try:
        # Get video info first
        info = get_video_info(url)
        print(f"Title: {info.get('title', 'Unknown')}")
        print(f"Duration: {info.get('duration', 0) // 60}:{info.get('duration', 0) % 60:02d}")
        print(f"Uploader: {info.get('uploader', 'Unknown')}\n")

        # Download the video
        subprocess.run(cmd, check=True)
        print(f"\n✅ Download complete!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error downloading video: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def main():
    default_dir = get_default_download_dir()

    parser = argparse.ArgumentParser(
        description="Download YouTube videos with customizable quality and format"
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "-o", "--output",
        default=default_dir,
        help=f"Output directory (default: {default_dir})"
    )
    parser.add_argument(
        "-q", "--quality",
        default="best",
        choices=["best", "1080p", "720p", "480p", "360p", "worst"],
        help="Video quality (default: best)"
    )
    parser.add_argument(
        "-f", "--format",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="Video format (default: mp4)"
    )
    parser.add_argument(
        "-a", "--audio-only",
        action="store_true",
        help="Download only audio as MP3"
    )

    args = parser.parse_args()

    success = download_video(
        url=args.url,
        output_path=args.output,
        quality=args.quality,
        format_type=args.format,
        audio_only=args.audio_only
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()