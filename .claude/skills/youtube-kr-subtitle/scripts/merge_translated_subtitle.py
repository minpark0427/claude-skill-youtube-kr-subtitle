"""번역된 텍스트를 원본 SRT의 타임스탬프와 병합하는 스크립트"""
import sys
import json
import pysrt


def merge_translated_subtitle(original_srt_path, translated_texts, output_srt_path):
    """
    원본 SRT 파일의 타임스탬프와 번역된 텍스트를 병합하여 새 SRT 파일을 생성합니다.

    Args:
        original_srt_path (str): 원본 SRT 파일 경로 (타임스탬프 정보 포함)
        translated_texts (list): 번역된 텍스트 리스트
        output_srt_path (str): 출력 SRT 파일 경로

    Returns:
        dict: {
            'success': bool,
            'subtitle_count': int,
            'output_path': str
        }
    """
    # 원본 자막 로드
    print(f"원본 자막 로드 중: {original_srt_path}", file=sys.stderr)
    subs = pysrt.open(original_srt_path)

    if len(subs) != len(translated_texts):
        error_msg = f"자막 개수 불일치: 원본 {len(subs)}개 vs 번역 {len(translated_texts)}개"
        print(f"오류: {error_msg}", file=sys.stderr)
        return {
            'success': False,
            'error': error_msg,
            'subtitle_count': 0,
            'output_path': None
        }

    # 텍스트만 교체
    for i, translated_text in enumerate(translated_texts):
        subs[i].text = translated_text

    # 새 SRT 파일로 저장
    subs.save(output_srt_path, encoding='utf-8')
    print(f"✓ 번역된 자막 저장 완료: {output_srt_path}", file=sys.stderr)
    print(f"✓ 총 {len(subs)}개의 자막 항목 처리", file=sys.stderr)

    return {
        'success': True,
        'subtitle_count': len(subs),
        'output_path': output_srt_path
    }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python merge_translated_subtitle.py <original_srt> <translated_json> <output_srt>", file=sys.stderr)
        print("\nExample:", file=sys.stderr)
        print('  python merge_translated_subtitle.py video.en.srt translated.json video.ko.srt', file=sys.stderr)
        print("\ntranslated_json should be a JSON array of translated strings", file=sys.stderr)
        sys.exit(1)

    original_srt = sys.argv[1]
    translated_json_path = sys.argv[2]
    output_srt = sys.argv[3]

    # 번역된 텍스트 로드
    with open(translated_json_path, 'r', encoding='utf-8') as f:
        translated_texts = json.load(f)

    if not isinstance(translated_texts, list):
        print("오류: translated_json은 문자열 배열이어야 합니다.", file=sys.stderr)
        sys.exit(1)

    result = merge_translated_subtitle(original_srt, translated_texts, output_srt)

    # 결과 출력
    print(json.dumps(result, indent=2, ensure_ascii=False))
