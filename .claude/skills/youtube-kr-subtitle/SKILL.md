---
name: youtube-kr-subtitle
description: Download YouTube videos, extract English subtitles, and translate them to Korean with two options - (1) Quick automated Google Translate or (2) High-quality Claude translation with full context awareness. Burns Korean subtitles into the video. Use this skill when the user requests Korean subtitle insertion for YouTube videos or asks to translate YouTube content to Korean.
---

# YouTube Korean Subtitle Translator

## Overview

This skill enables Claude to download YouTube videos and create new versions with Korean subtitles burned directly into the video. It offers **two translation methods**:

1. **Quick Path:** Fast automated translation using Google Translate (1-2 minutes)
2. **Quality Path:** Context-aware manual translation by Claude (30-45 minutes, recommended)

The Quality Path leverages Claude's own translation capabilities with full context awareness - including video metadata, web research about the content, and understanding of the subject matter - providing superior quality for professional use.

## When to Use This Skill

Use this skill when users request:
- "Add Korean subtitles to this YouTube video: [URL]"
- "Translate this YouTube video to Korean"
- "Download this video and burn Korean subtitles into it"
- "Create a Korean version of this YouTube video"

## Workflow

### Step 0: Environment Setup Check (First Time Only)

Before processing any videos, verify that the environment is properly configured:

```bash
python scripts/setup_check.py
```

This script checks:
- Python version (3.7+)
- Virtual environment existence
- Required packages (yt-dlp, pysrt, ffmpeg-python, deep-translator)
- FFmpeg installation

**Auto-fix mode:** To automatically create venv and install packages:
```bash
python scripts/setup_check.py --auto-fix
```

**Output:** JSON containing:
- `success`: boolean indicating if all checks passed
- `results`: detailed information about each component
- `actions_taken`: list of automatic fixes performed (if --auto-fix used)

**What the script does in auto-fix mode:**
1. Creates virtual environment if it doesn't exist
2. Installs all required Python packages from requirements.txt
3. Verifies FFmpeg is installed (provides installation instructions if not)

**Error Handling:** If FFmpeg is not installed, the script will provide platform-specific installation commands. FFmpeg cannot be auto-installed and must be installed manually.

**Important:** Run this check before your first video processing. Once the environment is set up, you don't need to run this again unless you encounter dependency issues.

### Step 1: Download Video and Subtitles

**First, create a dedicated project directory for this video:**

```bash
# Extract video ID from URL or use timestamp
VIDEO_ID="m24gQmtUFaA"  # Example from URL
PROJECT_DIR="projects/${VIDEO_ID}"
mkdir -p "${PROJECT_DIR}"
```

**Then run the download script to fetch the YouTube video, English subtitles, and metadata:**

```bash
python scripts/download_youtube.py "<youtube_url>" "${PROJECT_DIR}/"
```

**Output:** JSON containing:
- `video_path`: Downloaded video file path (e.g., `projects/m24gQmtUFaA/video.mp4`)
- `subtitle_path`: English subtitle SRT file path (e.g., `projects/m24gQmtUFaA/video.en.srt`)
- `title`: Video title
- `description`: Video description
- `duration`: Video duration in seconds
- `video_id`: YouTube video ID
- `project_dir`: The created project directory path

**Project Directory Structure:**
```
projects/m24gQmtUFaA/
├── video.mp4                    # Downloaded video
├── video.en.srt                 # English subtitles
├── subtitle_texts.json          # Extracted texts (Step 2)
├── video_context.md             # Translation context (Step 3)
├── translated_texts.json        # Korean translations (Step 4)
├── video.ko.srt                 # Korean subtitle SRT (Step 5)
└── video_korean.mp4             # Final output (Step 6)
```

**Error Handling:** If `subtitle_path` is null, inform the user that the video lacks English subtitles and cannot be processed in the current version.

### Step 2: Extract Subtitle Text

Extract only the text content from the SRT file for translation:

```bash
python scripts/extract_subtitle_text.py "${PROJECT_DIR}/video.en.srt" > "${PROJECT_DIR}/subtitle_texts.json"
```

**Output:** JSON containing:
- `texts`: Array of subtitle text strings (preprocessed and grouped into sentences)
- `metadata.total_count`: Number of subtitle entries
- `metadata.processed_count`: Number after preprocessing (overlap fixes, grouping)

**Important:** The script automatically:
- Fixes overlapping timestamps (YouTube's rolling caption format)
- Removes short duplicate subtitles (<150ms)
- Groups consecutive subtitles into sentence units for better translation context

### Step 2.5: Choose Translation Method

**Before proceeding, ask the user to choose their preferred translation approach:**

```
I've extracted [N] subtitle entries from the video.

How would you like me to translate these to Korean?

Option 1: Quick Automated Translation (Google Translate)
  ✅ Pros: Very fast (1-2 minutes)
  ❌ Cons: Lower quality, mistranslations, no context awareness
  📊 Best for: Quick previews, personal use, non-critical content

Option 2: High-Quality Claude Translation (Recommended)
  ✅ Pros: Context-aware, accurate terminology, cultural adaptation
  ❌ Cons: Takes longer (30-45 minutes for ~400 entries)
  📊 Best for: Professional use, publishing, technical/educational content

Which would you prefer? (1 or 2)
```

**Based on the user's choice:**
- **If Option 1 (Quick):** Skip to Step 4b (Automated Translation)
- **If Option 2 (Quality):** Continue to Step 3 (Context Gathering)

### Step 3: Gather Context for Translation (Quality Path Only)

Before translating, build comprehensive context to ensure high-quality, contextually-aware translation:

#### 3a. Analyze Video Metadata

Review the video title and description from Step 1. Identify:
- Subject matter (technology, education, entertainment, etc.)
- Key topics or themes
- Technical terminology that may require specialized translation
- Tone and style (formal, casual, educational, etc.)

#### 3b. Web Search for Additional Context

Perform web searches to understand the content better:

```
Search queries to consider:
- "[video_title]" - Find related content and context
- "[key_topics] Korean translation" - Find established Korean terminology
- "[subject_matter] 한글 용어" - Find domain-specific Korean terms
```

Save findings to a context file for reference during translation.

#### 3c. Create Translation Context File

Write a context file in the project directory (`${PROJECT_DIR}/video_context.md`) containing:

```markdown
# Translation Context for [Video Title]

## Video Overview
- **Title:** [title]
- **Subject:** [subject matter]
- **Duration:** [duration]
- **Key Topics:** [list of main topics]

## Key Terminology
[Table of English terms and their appropriate Korean translations]

## Tone and Style
[Description of the appropriate translation style]

## Additional Notes
[Any web research findings, cultural considerations, or translation guidelines]
```

### Step 4a: Translate Subtitles with Claude (Quality Path)

Now perform the actual translation using the context gathered above. This is where Claude's capabilities shine:

**Translation Guidelines:**
1. Read the context file created in Step 3c
2. Review the first few subtitle texts to understand the flow
3. Translate each subtitle text to Korean, considering:
   - **Context awareness:** Use video metadata and web research findings
   - **Terminology consistency:** Apply terms from the context file
   - **Sentence flow:** Maintain natural Korean sentence structure
   - **Cultural adaptation:** Adapt idioms and cultural references appropriately
   - **Length consideration:** Keep translations reasonably similar in length to fit subtitle timing
4. Maintain the exact same number of entries as the input array

**Output Format:** Create a JSON array of translated strings and save it:

```json
[
  "첫 번째 번역된 자막",
  "두 번째 번역된 자막",
  "세 번째 번역된 자막"
]
```

Save this to the project directory: `${PROJECT_DIR}/translated_texts.json`

**Quality Checks:**
- Verify the array length matches the original subtitle count
- Ensure no entries are empty (unless the original was empty)
- Check that technical terms are consistently translated
- Confirm the tone matches the video's style

### Step 4b: Automated Translation (Quick Path)

**Alternative quick translation method using automated tools:**

Create a Python script using `deep-translator` for automated Google Translate:

```python
from deep_translator import GoogleTranslator
import json
import os

# Set your project directory
PROJECT_DIR = "projects/m24gQmtUFaA"  # Use actual video ID

# Load subtitle texts from Step 2
with open(f'{PROJECT_DIR}/subtitle_texts.json', 'r') as f:
    texts = json.load(f)['texts']

# Translate using Google Translate
translator = GoogleTranslator(source='en', target='ko')
translated = []

for i, text in enumerate(texts):
    if text.strip():
        translated.append(translator.translate(text))
    else:
        translated.append(text)

    if (i + 1) % 10 == 0:
        print(f"Progress: {i + 1}/{len(texts)}")

# Save translated texts to project directory
with open(f'{PROJECT_DIR}/translated_texts.json', 'w', encoding='utf-8') as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)
```

**⚠️ Important Limitations:**
- No context awareness or terminology consistency
- May produce mistranslations, especially for technical content
- Not suitable for professional or published content
- Recommended only for quick previews or personal use

**Output:** Same format as Step 4a - JSON array of translated strings saved to `translated_texts.json`

### Step 5: Merge Translated Text with SRT Timestamps

Combine the translated texts with the original SRT timing information:

```bash
python scripts/merge_translated_subtitle.py <original_srt> <translated_json> <output_srt>
```

**Example:**
```bash
python scripts/merge_translated_subtitle.py \
  "${PROJECT_DIR}/video.en.srt" \
  "${PROJECT_DIR}/translated_texts.json" \
  "${PROJECT_DIR}/video.ko.srt"
```

**Output:** JSON containing:
- `success`: boolean
- `subtitle_count`: number of subtitles processed
- `output_path`: path to Korean SRT file

### Step 6: Burn Subtitles into Video

Use FFmpeg to hardcode the Korean subtitles into the video:

```bash
python scripts/process_video.py <video_path> <korean_srt> <output_path> [font_name] [font_size]
```

**Example:**
```bash
python scripts/process_video.py \
  "${PROJECT_DIR}/video.mp4" \
  "${PROJECT_DIR}/video.ko.srt" \
  "${PROJECT_DIR}/video_korean.mp4" \
  Arial 16
```

**Font Size Guidelines for Korean Text:**
- **FontSize=16** - Recommended default (good readability without being intrusive)
- **FontSize=14** - Smaller, for videos with lots of on-screen text
- **FontSize=18** - Slightly larger, for longer viewing distances
- **FontSize=20-24** - Large, only for accessibility or specific requirements

**Note:** Korean characters are typically more complex than Latin characters, so they appear larger at the same font size. A font size of 16-18 for Korean provides similar visual weight to 20-24 for English text.

**Output:** JSON containing:
- `success`: boolean
- `output_path`: path to final video with Korean subtitles
- `file_size_mb`: size of output file
- `font_settings`: applied font name and size

**Note:** FFmpeg must be installed on the system. The script checks for FFmpeg availability and provides installation instructions if needed.

## Complete Example Workflow

```bash
# 0. Check environment setup (first time only)
python scripts/setup_check.py --auto-fix

# 1. Create project directory and download video
VIDEO_ID="m24gQmtUFaA"
PROJECT_DIR="projects/${VIDEO_ID}"
mkdir -p "${PROJECT_DIR}"
python scripts/download_youtube.py "https://www.youtube.com/watch?v=${VIDEO_ID}" "${PROJECT_DIR}/"

# 2. Extract subtitle texts
python scripts/extract_subtitle_text.py "${PROJECT_DIR}/video.en.srt" > "${PROJECT_DIR}/subtitle_texts.json"

# 2.5. Choose translation method (user decision)
# Option 1: Quick automated translation (Step 4b)
# Option 2: Quality Claude translation (Steps 3-4a)

# [IF OPTION 2 CHOSEN]
# 3. Gather context (manual step by Claude)
# - Analyze video metadata
# - Perform web searches
# - Create ${PROJECT_DIR}/video_context.md

# 4a. Translate with Claude (manual step)
# - Read context file
# - Translate each subtitle text
# - Save to ${PROJECT_DIR}/translated_texts.json

# [IF OPTION 1 CHOSEN]
# 4b. Run automated translation script (saves to same location)

# 5. Merge translations with timestamps
python scripts/merge_translated_subtitle.py \
  "${PROJECT_DIR}/video.en.srt" \
  "${PROJECT_DIR}/translated_texts.json" \
  "${PROJECT_DIR}/video.ko.srt"

# 6. Burn subtitles into video (with recommended font size for Korean)
python scripts/process_video.py \
  "${PROJECT_DIR}/video.mp4" \
  "${PROJECT_DIR}/video.ko.srt" \
  "${PROJECT_DIR}/video_korean.mp4" \
  Arial 16

# Final output: projects/m24gQmtUFaA/video_korean.mp4
```

## Key Advantages Over Automated Translation

This skill offers **two translation approaches**:

### Quality Path (Option 2 - Recommended)
Superior translation quality through Claude's capabilities:

1. **Context-Aware:** Claude understands the video's subject matter through metadata and web research
2. **Terminology Consistency:** Establishes and maintains consistent translation of key terms
3. **Cultural Adaptation:** Adapts content appropriately for Korean audiences
4. **Tone Matching:** Maintains the original video's tone and style
5. **Quality Control:** Claude can review and refine translations before finalizing

### Quick Path (Option 1 - Fast but Lower Quality)
Automated Google Translate for speed:

1. **Speed:** Translates 400+ entries in 1-2 minutes
2. **Simplicity:** No manual translation required
3. **Trade-offs:** Lower accuracy, no context awareness, potential mistranslations

**Recommendation:** Use Quality Path for any content that will be shared, published, or used professionally. Use Quick Path only for personal previews or non-critical content.

## Prerequisites

The following must be installed on the system:
- Python 3.7+
- FFmpeg (for video processing)
- Python packages: `yt-dlp`, `pysrt`

Install Python dependencies:
```bash
pip install yt-dlp pysrt
```

Install FFmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## Limitations

- Only processes videos with existing English subtitles (auto-generated or manual)
- Videos without subtitles are not currently supported
- Processing time depends on video length and translation thoroughness
- Large videos may take significant time for FFmpeg encoding

## Scripts Reference

### scripts/download_youtube.py
Downloads YouTube video and English subtitles, returns metadata including title and description.

### scripts/extract_subtitle_text.py
Preprocesses SRT file and extracts text array for translation. Automatically handles YouTube's overlapping timestamp format.

### scripts/merge_translated_subtitle.py
Combines translated text array with original SRT timing information to create Korean SRT file.

### scripts/process_video.py
Uses FFmpeg to burn Korean subtitles into the video with customizable font styling.
