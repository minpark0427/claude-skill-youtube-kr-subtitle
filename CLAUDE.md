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

### Running the Application
```bash
# Basic usage with default URL
python main.py

# With custom YouTube URL
python main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Prerequisites
FFmpeg must be installed on the system:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## Architecture

### Processing Pipeline
The application follows a strict 5-stage sequential pipeline (main.py:14-97):

1. **Video Download** (youtube_downloader.py) - Uses yt-dlp to download video from YouTube
2. **Subtitle Download** (youtube_downloader.py) - Extracts English subtitles (en, en-US, en-GB)
3. **Translation** (translator.py) - Translates subtitles to Korean using Google Translate
4. **Subtitle Processing** (subtitle_processor.py) - Fixes overlapping timestamps and merges short subtitles
5. **Video Processing** (video_processor.py) - Burns Korean subtitles into video using FFmpeg

### Module Responsibilities

**youtube_downloader.py**
- `download_video()`: Downloads YouTube video to downloads/ directory using yt-dlp
- `download_subtitles()`: Downloads English subtitles, tries en, en-US, en-GB in order
- Returns video metadata (title, duration, video_id) for downstream processing

**subtitle_processor.py**
- Critical module that handles YouTube's unique subtitle format issue
- `fix_overlapping_subtitles()`: YouTube auto-generated subtitles use 2-line rolling caption style where timestamps intentionally overlap. This function adjusts each subtitle's end time to 1ms before the next subtitle's start time (lines 6-40)
- `remove_short_duplicates()`: Removes subtitles shorter than 150ms that have duplicate text (lines 43-72)
- `group_subtitles()`: Merges consecutive subtitles into sentence units based on max 300ms gap and max 150 chars length (lines 75-123)
- `load_subtitle()`: Entry point that applies all three preprocessing steps automatically (lines 126-149)

**translator.py**
- `translate_texts()`: Batch translates text list using Google Translate API
- Includes retry logic (3 attempts), rate limiting (0.2s delay between calls), and text cleaning
- Falls back to original text if translation fails
- `translate_subtitle_file()`: Orchestrates the full subtitle translation workflow

**video_processor.py**
- `burn_subtitles()`: Uses FFmpeg to hardcode subtitles into video
- Applies force_style for consistent Korean subtitle appearance: white text (&HFFFFFF), black outline (&H000000), semi-transparent background (&H80000000)
- Audio stream is copied without re-encoding for faster processing
- `check_ffmpeg()`: Validates FFmpeg installation before processing

### Data Flow

```
YouTube URL
    ↓
downloads/{title}.mp4 (video)
downloads/{title}.en.srt (original subtitles)
    ↓ subtitle_processor.load_subtitle()
Fixed & merged subtitles
    ↓ translator.translate_subtitle_file()
downloads/{title}.en.ko.srt (Korean subtitles)
    ↓ video_processor.burn_subtitles()
output/{title}_ko_{timestamp}.mp4 (final video)
```

### Directory Structure
- `src/` - All Python modules
- `downloads/` - Temporary storage for downloaded videos and original subtitles
- `output/` - Final processed videos with Korean subtitles
- `venv/` - Python virtual environment (gitignored)

## Known Issues & Limitations

### Subtitle Overlap Problem (Automatically Fixed)
YouTube auto-generated subtitles intentionally use overlapping timestamps for rolling captions. The subtitle_processor module automatically detects and fixes this by adjusting end times to prevent multiple captions displaying simultaneously.

### Current Limitations
- Only processes videos with existing English subtitles (auto-generated or manual)
- Videos without subtitles are not supported in current version
- Translation quality depends on Google Translate API
- Rate limiting: 0.2s delay between translation calls may slow processing for long videos
- No support for custom subtitle styling beyond hardcoded defaults

## Future Enhancements (See PLAN.md)

Phase 1 planned features:
- Whisper STT integration for videos without existing subtitles
- GPT translation option for higher quality
- Customizable subtitle styling (font, color, position)
- Web UI

## Important Implementation Notes

### Subtitle Timestamp Handling
When modifying subtitle_processor.py, be aware that YouTube's rolling caption format requires special handling. The fix_overlapping_subtitles() function implements an industry-standard algorithm to ensure clean subtitle display. Do not remove or bypass this preprocessing step.

### FFmpeg Path Escaping
The burn_subtitles() function includes special path escaping logic (line 36) to handle Windows paths and special characters. Maintain this escaping when modifying FFmpeg commands.

### Translation Retry Logic
The translator module includes 3-attempt retry logic and 0.2s rate limiting. These values balance reliability and performance - adjust carefully if modifying.

### Virtual Environment Usage
Always work within the venv. The project uses standard Python packages but requires FFmpeg system dependency which is not managed by pip.
