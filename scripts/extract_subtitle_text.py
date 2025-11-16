#!/usr/bin/env python3
"""
Extract subtitle text from SRT file for translation.
Usage: python scripts/extract_subtitle_text.py <subtitle_path>
"""

import sys
import json
import pysrt

def fix_overlapping_subtitles(subs):
    """Fix overlapping timestamps in YouTube auto-generated subtitles."""
    for i in range(len(subs) - 1):
        current = subs[i]
        next_sub = subs[i + 1]

        # If current subtitle ends after next one starts, adjust end time
        if current.end > next_sub.start:
            # Set end time to 1ms before next subtitle starts
            current.end.shift(milliseconds=-(current.end.ordinal - next_sub.start.ordinal + 1))

    return subs

def remove_short_duplicates(subs, min_duration_ms=150):
    """Remove very short subtitles that have duplicate text."""
    filtered = []
    prev_text = None

    for sub in subs:
        duration_ms = (sub.end.ordinal - sub.start.ordinal)
        text = sub.text.strip()

        # Keep if duration is long enough or text is different from previous
        if duration_ms >= min_duration_ms or text != prev_text:
            filtered.append(sub)
            prev_text = text

    return pysrt.SubRipFile(items=filtered)

def group_subtitles(subs, max_gap_ms=300, max_length=150):
    """Group consecutive subtitles into sentence units."""
    if not subs:
        return pysrt.SubRipFile()

    grouped = []
    current_group = {
        'start': subs[0].start,
        'end': subs[0].end,
        'text': subs[0].text.strip()
    }

    for i in range(1, len(subs)):
        sub = subs[i]
        gap_ms = sub.start.ordinal - current_group['end'].ordinal
        combined_text = current_group['text'] + ' ' + sub.text.strip()

        # Check if we should continue grouping
        if gap_ms <= max_gap_ms and len(combined_text) <= max_length:
            # Extend current group
            current_group['end'] = sub.end
            current_group['text'] = combined_text
        else:
            # Save current group and start new one
            grouped.append(pysrt.SubRipItem(
                index=len(grouped) + 1,
                start=current_group['start'],
                end=current_group['end'],
                text=current_group['text']
            ))
            current_group = {
                'start': sub.start,
                'end': sub.end,
                'text': sub.text.strip()
            }

    # Add final group
    grouped.append(pysrt.SubRipItem(
        index=len(grouped) + 1,
        start=current_group['start'],
        end=current_group['end'],
        text=current_group['text']
    ))

    return pysrt.SubRipFile(items=grouped)

def extract_subtitle_texts(subtitle_path):
    """Extract and preprocess subtitle texts."""
    # Load subtitle file
    subs = pysrt.open(subtitle_path)
    original_count = len(subs)

    # Apply preprocessing
    subs = fix_overlapping_subtitles(subs)
    subs = remove_short_duplicates(subs)
    subs = group_subtitles(subs)

    # Extract text array
    texts = [sub.text.strip() for sub in subs]

    return {
        'texts': texts,
        'metadata': {
            'total_count': original_count,
            'processed_count': len(texts)
        }
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/extract_subtitle_text.py <subtitle_path>")
        sys.exit(1)

    subtitle_path = sys.argv[1]

    try:
        result = extract_subtitle_texts(subtitle_path)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'error': str(e)}, indent=2), file=sys.stderr)
        sys.exit(1)
