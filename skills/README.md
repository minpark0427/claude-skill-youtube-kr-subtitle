# YouTube Korean Subtitle Skills

This directory contains Claude Code skills for automated YouTube video processing with Korean subtitle insertion.

## Available Skills

### youtube-kr-subtitle

Download YouTube videos, extract English subtitles, translate to Korean using Claude's translation capabilities (with video context and web search), and burn Korean subtitles into the video.

**Location:** `skills/youtube-kr-subtitle/`

**Usage:**
- Invoke the skill when users request Korean subtitle insertion for YouTube videos
- The skill automatically activates for requests like:
  - "Add Korean subtitles to this YouTube video: [URL]"
  - "Translate this YouTube video to Korean"
  - "Create a Korean version of this video"

## Skill Structure

Each skill follows the Anthropic Skills standard:

```
skills/
└── youtube-kr-subtitle/
    ├── SKILL.md              # Skill definition with YAML frontmatter and instructions
    ├── scripts/              # Python scripts for processing pipeline
    │   ├── download_youtube.py
    │   ├── extract_subtitle_text.py
    │   ├── merge_translated_subtitle.py
    │   └── process_video.py
    ├── assets/               # Additional resources
    └── references/           # Reference documentation
```

## Integration with Claude Code

This skill is configured for both:

1. **Project Skills**: Available when working in this repository
2. **Plugin Skills**: Can be packaged and shared as a plugin

### Project Skills Setup

The `.claude/skills/` directory contains symlinks to skills in this directory, making them available to Claude Code when working in this project.

### Plugin Distribution

Skills can be packaged and distributed as plugins for use across different projects. See the Anthropic Skills repository for packaging guidelines.

## Prerequisites

### System Requirements
- Python 3.7+
- FFmpeg (for video processing)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- `yt-dlp` - YouTube video/subtitle download
- `pysrt` - SRT subtitle file parsing

### FFmpeg Installation
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

## Skill Development

### Creating New Skills

1. Create a new directory under `skills/`
2. Add a `SKILL.md` file with YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description of skill purpose and when to use it
   ---
   ```
3. Include instructions, examples, and guidelines in the markdown body
4. Add any supporting scripts or resources

### Best Practices

- Keep skills self-contained within their directories
- Include practical examples demonstrating skill usage
- Provide clear guidelines for consistent application
- Test thoroughly before deployment
- Document prerequisites and system requirements

## References

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code)
- [Skill Creation Guide](https://github.com/anthropics/skills/tree/main/template-skill)

## License

This skill is provided for demonstration and educational purposes. Test thoroughly in your own environment before relying on it for critical tasks.
