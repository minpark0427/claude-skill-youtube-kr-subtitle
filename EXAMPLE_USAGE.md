# Working Directory Example

## Before (Old Behavior)
When you ran the skill, projects were created inside the skill's directory:
```
/Users/my/.claude/skills/youtube-kr-subtitle/
└── projects/
    └── VIDEO_ID/
        ├── video.mp4
        ├── video.en.srt
        └── ...
```

## After (New Behavior)
Now projects are created in YOUR current working directory:

### Example Scenario 1: Working from Home Directory
```bash
cd ~/my-youtube-projects
# Now run Claude Code and use the skill
# Result: projects are created here
```

Directory structure:
```
/Users/my/my-youtube-projects/
└── projects/
    └── VIDEO_ID/
        ├── video.mp4
        ├── video.en.srt
        └── video_korean.mp4
```

### Example Scenario 2: Working from Desktop
```bash
cd ~/Desktop
# Now run Claude Code and use the skill
# Result: projects are created on Desktop
```

Directory structure:
```
/Users/my/Desktop/
└── projects/
    └── VIDEO_ID/
        ├── video.mp4
        └── ...
```

## How It Works

The skill now uses:
- **Absolute paths for scripts**: `~/.claude/skills/youtube-kr-subtitle/scripts/download_youtube.py`
- **Relative paths for projects**: `./projects/VIDEO_ID/`

This means:
1. Scripts are always found (using absolute path to skill directory)
2. Projects are created in your current location (using relative path)
3. You can organize your subtitle projects anywhere on your system
