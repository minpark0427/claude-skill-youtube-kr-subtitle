#!/usr/bin/env python3
"""
Merge translated text with original SRT timestamps.
Usage: python scripts/merge_translated_subtitle.py <original_srt> <translated_json> <output_srt>
"""

import sys
import json
import pysrt

def merge_translations(original_srt_path, translated_json_path, output_srt_path):
    """Merge translated texts with original SRT timing."""
    # Load original SRT with preprocessing (to match extract_subtitle_text.py)
    from extract_subtitle_text import fix_overlapping_subtitles, remove_short_duplicates, group_subtitles

    subs = pysrt.open(original_srt_path)
    subs = fix_overlapping_subtitles(subs)
    subs = remove_short_duplicates(subs)
    subs = group_subtitles(subs)

    # Load translated texts
    with open(translated_json_path, 'r', encoding='utf-8') as f:
        translated_texts = json.load(f)

    # Verify counts match
    if len(subs) != len(translated_texts):
        raise ValueError(
            f"Mismatch: {len(subs)} subtitles but {len(translated_texts)} translations"
        )

    # Create new SRT with translated text
    new_subs = pysrt.SubRipFile()
    for i, sub in enumerate(subs):
        new_sub = pysrt.SubRipItem(
            index=i + 1,
            start=sub.start,
            end=sub.end,
            text=translated_texts[i]
        )
        new_subs.append(new_sub)

    # Save to output file
    new_subs.save(output_srt_path, encoding='utf-8')

    return {
        'success': True,
        'subtitle_count': len(new_subs),
        'output_path': output_srt_path
    }

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python scripts/merge_translated_subtitle.py <original_srt> <translated_json> <output_srt>")
        sys.exit(1)

    original_srt = sys.argv[1]
    translated_json = sys.argv[2]
    output_srt = sys.argv[3]

    try:
        result = merge_translations(original_srt, translated_json, output_srt)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
