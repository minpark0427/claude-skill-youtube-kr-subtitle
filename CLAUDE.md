# CLAUDE.md

This repository provides the `youtube-kr-subtitle` skill for Claude Code. **All detailed workflow instructions are in `.claude/skills/youtube-kr-subtitle/SKILL.md`.**

## Project Overview

YouTube Korean Subtitle Auto-Insertion Service - Downloads YouTube videos, translates English subtitles to Korean using Claude's context-aware translation, and burns Korean subtitles into the video.

## Quick Start

```bash
# First-time setup (auto-configures environment)
python3 .claude/skills/youtube-kr-subtitle/scripts/setup_check.py --auto-fix

# Or use the skill directly in Claude Code
"Add Korean subtitles to this YouTube video: <youtube_url>"
```

## Prerequisites

- **Python 3.7+** (auto-checked by setup_check.py)
- **FFmpeg** (must be installed manually):
  ```bash
  brew install ffmpeg              # macOS
  sudo apt-get install ffmpeg      # Ubuntu/Debian
  ```

## Key Implementation Notes

When working with this codebase, always remember:

1. **Use SKILL.md as primary reference** - The complete workflow, script documentation, and usage instructions are in `.claude/skills/youtube-kr-subtitle/SKILL.md`

2. **Subtitle preprocessing is critical** - `extract_subtitle_text.py` fixes YouTube's overlapping timestamp format. Never bypass this step.

3. **Translation count must match** - `merge_translated_subtitle.py` validates that translation array length equals preprocessed subtitle count.

4. **Virtual environment required** - All scripts expect to run within `venv/` with dependencies from `requirements.txt`.
