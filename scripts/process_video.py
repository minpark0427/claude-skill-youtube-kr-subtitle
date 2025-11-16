#!/usr/bin/env python3
"""
Burn subtitles into video using FFmpeg.
Usage: python scripts/process_video.py <video_path> <subtitle_path> <output_path> [font_name] [font_size]
"""

import sys
import os
import json
import subprocess
import shutil

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    if not shutil.which('ffmpeg'):
        raise RuntimeError(
            "FFmpeg not found. Please install FFmpeg:\n"
            "  macOS: brew install ffmpeg\n"
            "  Ubuntu/Debian: sudo apt-get install ffmpeg"
        )

def burn_subtitles(video_path, subtitle_path, output_path, font_name='Arial', font_size=24):
    """Burn subtitles into video using FFmpeg."""
    check_ffmpeg()

    # Escape subtitle path for FFmpeg (Windows/special chars)
    if sys.platform == 'win32':
        subtitle_filter = subtitle_path.replace('\\', '/').replace(':', '\\\\:')
    else:
        subtitle_filter = subtitle_path.replace(':', '\\:')

    # FFmpeg command with Korean subtitle styling
    force_style = (
        f"FontName={font_name},"
        f"FontSize={font_size},"
        "PrimaryColour=&HFFFFFF,"  # White text
        "OutlineColour=&H000000,"  # Black outline
        "BackColour=&H80000000,"   # Semi-transparent black background
        "BorderStyle=1,"
        "Outline=2,"
        "Shadow=0,"
        "MarginV=20"
    )

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={subtitle_filter}:force_style='{force_style}'",
        '-c:a', 'copy',  # Copy audio without re-encoding
        '-y',  # Overwrite output file
        output_path
    ]

    # Run FFmpeg
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")

    # Get output file size
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

    return {
        'success': True,
        'output_path': output_path,
        'file_size_mb': round(file_size_mb, 2)
    }

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python scripts/process_video.py <video_path> <subtitle_path> <output_path> [font_name] [font_size]")
        sys.exit(1)

    video_path = sys.argv[1]
    subtitle_path = sys.argv[2]
    output_path = sys.argv[3]
    font_name = sys.argv[4] if len(sys.argv) > 4 else 'Arial'
    font_size = int(sys.argv[5]) if len(sys.argv) > 5 else 24

    try:
        result = burn_subtitles(video_path, subtitle_path, output_path, font_name, font_size)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
