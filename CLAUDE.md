# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

YouTube Korean Subtitle Auto-Insertion Service - A Python application that automatically downloads YouTube videos, extracts/generates English subtitles, translates them to Korean, and burns the Korean subtitles directly into the video using FFmpeg.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Prerequisites
FFmpeg must be installed on the system:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### Running the Scripts
The application uses a modular script-based workflow:

```bash
# 1. Download video and subtitles
python scripts/download_youtube.py "<youtube_url>" downloads/

# 2. Extract subtitle texts
python scripts/extract_subtitle_text.py downloads/VideoTitle.en.srt > subtitle_texts.json

# 3. Translate (manual or external API)
# Translate the texts array to Korean and save as translated_texts.json

# 4. Merge translations with timestamps
python scripts/merge_translated_subtitle.py \
  downloads/VideoTitle.en.srt \
  translated_texts.json \
  downloads/VideoTitle.ko.srt

# 5. Burn subtitles into video
python scripts/process_video.py \
  downloads/VideoTitle.mp4 \
  downloads/VideoTitle.ko.srt \
  output/VideoTitle_korean.mp4
```

## Architecture

### Processing Pipeline
The application uses a modular script-based workflow with 5 stages:

1. **Video Download** (scripts/download_youtube.py) - Uses yt-dlp to download video and English subtitles
2. **Subtitle Extraction** (scripts/extract_subtitle_text.py) - Preprocesses subtitles and extracts text array
3. **Translation** (External/Manual) - Translate texts to Korean (manual or using external APIs)
4. **Subtitle Merging** (scripts/merge_translated_subtitle.py) - Combines translations with original timestamps
5. **Video Processing** (scripts/process_video.py) - Burns Korean subtitles into video using FFmpeg

### Script Responsibilities

**scripts/download_youtube.py**
- Downloads YouTube video and English subtitles using yt-dlp
- Tries multiple English subtitle variants (en, en-US, en-GB)
- Returns JSON with video metadata (video_path, subtitle_path, title, description, duration, video_id)

**scripts/extract_subtitle_text.py**
- Critical script that handles YouTube's unique subtitle format issue
- `fix_overlapping_subtitles()`: YouTube auto-generated subtitles use 2-line rolling caption style where timestamps intentionally overlap. Adjusts each subtitle's end time to 1ms before the next subtitle's start time
- `remove_short_duplicates()`: Removes subtitles shorter than 150ms that have duplicate text
- `group_subtitles()`: Merges consecutive subtitles into sentence units (max 300ms gap, max 150 chars)
- Returns JSON with preprocessed text array ready for translation

**scripts/merge_translated_subtitle.py**
- Merges translated text array with original SRT timestamps
- Applies same preprocessing as extract_subtitle_text.py to ensure alignment
- Creates Korean SRT file with proper timing
- Validates that translation count matches original subtitle count

**scripts/process_video.py**
- Uses FFmpeg to burn Korean subtitles into video
- Applies force_style for consistent appearance: white text (&HFFFFFF), black outline (&H000000), semi-transparent background (&H80000000)
- Audio stream is copied without re-encoding for faster processing
- Includes FFmpeg availability check and path escaping for special characters

### Data Flow

```
YouTube URL
    ↓ scripts/download_youtube.py
downloads/{title}.mp4 (video)
downloads/{title}.en.srt (original subtitles)
    ↓ scripts/extract_subtitle_text.py
subtitle_texts.json (preprocessed text array)
    ↓ Manual/External Translation
translated_texts.json (Korean text array)
    ↓ scripts/merge_translated_subtitle.py
downloads/{title}.ko.srt (Korean subtitles)
    ↓ scripts/process_video.py
output/{title}_korean_{timestamp}.mp4 (final video)
```

### Directory Structure
- `scripts/` - Modular Python scripts for each processing stage
- `downloads/` - Temporary storage for downloaded videos and original subtitles
- `output/` - Final processed videos with Korean subtitles
- `venv/` - Python virtual environment (gitignored)

## Known Issues & Limitations

### Subtitle Overlap Problem (Automatically Fixed)
YouTube auto-generated subtitles intentionally use overlapping timestamps for rolling captions. The extract_subtitle_text.py script automatically detects and fixes this by adjusting end times to prevent multiple captions displaying simultaneously.

### Current Limitations
- Only processes videos with existing English subtitles (auto-generated or manual)
- Videos without subtitles are not supported in current version
- Translation is handled externally (manual or external APIs)
- Long videos may take significant time for FFmpeg processing
- Subtitle styling is hardcoded (white text, black outline, semi-transparent background)

## Future Enhancements

Potential improvements:
- Whisper STT integration for videos without existing subtitles
- Automated translation API integration
- Customizable subtitle styling parameters (font, color, position, size)
- Batch processing support
- Web UI

## Important Implementation Notes

### Subtitle Timestamp Handling
The extract_subtitle_text.py script includes critical preprocessing logic for YouTube's rolling caption format. The fix_overlapping_subtitles() function implements an industry-standard algorithm. Do not remove or bypass this preprocessing step as it's essential for clean subtitle display.

### Translation Count Matching
The merge_translated_subtitle.py script validates that the number of translations exactly matches the number of preprocessed subtitles. This ensures proper alignment between Korean text and timing information.

### FFmpeg Path Escaping
The process_video.py script includes special path escaping logic to handle Windows paths and special characters (including colons in filenames). Maintain this escaping when modifying FFmpeg commands.

### Virtual Environment Usage
Always work within the venv. The project uses standard Python packages (yt-dlp, pysrt) but requires FFmpeg system dependency which must be installed separately.
