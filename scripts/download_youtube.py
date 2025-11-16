#!/usr/bin/env python3
"""
Download YouTube video and English subtitles.
Usage: python scripts/download_youtube.py "<youtube_url>" <output_dir>
"""

import sys
import os
import json
import yt_dlp

def download_video_and_subtitles(url, output_dir):
    """Download YouTube video and English subtitles."""
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        'format': 'best[ext=mp4]',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'en-US', 'en-GB'],
        'subtitlesformat': 'srt',
        'skip_download': False,
    }

    result = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract video info
        info = ydl.extract_info(url, download=True)

        title = info.get('title', 'video')
        video_id = info.get('id', '')
        duration = info.get('duration', 0)
        description = info.get('description', '')

        # Clean title for filename
        clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()

        video_path = os.path.join(output_dir, f"{clean_title}.mp4")

        # Check for subtitle file
        subtitle_path = None
        for lang in ['en', 'en-US', 'en-GB']:
            potential_sub = os.path.join(output_dir, f"{clean_title}.{lang}.srt")
            if os.path.exists(potential_sub):
                subtitle_path = potential_sub
                break

        result = {
            'video_path': video_path,
            'subtitle_path': subtitle_path,
            'title': title,
            'description': description,
            'duration': duration,
            'video_id': video_id
        }

    return result

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python scripts/download_youtube.py \"<youtube_url>\" <output_dir>")
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2]

    try:
        result = download_video_and_subtitles(url, output_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
