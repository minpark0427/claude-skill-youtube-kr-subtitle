"""자막 파일 처리 모듈"""
import pysrt
import os


def fix_overlapping_subtitles(subs):
    """
    겹치는 자막의 타임스탬프를 수정합니다.
    YouTube 자동 생성 자막은 의도적으로 겹치는 타임스탬프를 가지고 있어
    화면에 여러 자막이 동시에 표시되는 문제가 발생합니다.

    해결 방법: 각 자막의 종료 시간이 다음 자막의 시작 시간보다 늦으면
    현재 자막의 종료 시간을 다음 자막 시작 직전으로 조정합니다.

    Args:
        subs (SubRipFile): 자막 객체

    Returns:
        SubRipFile: 수정된 자막 객체
    """
    fixed_count = 0

    for i in range(len(subs) - 1):
        current_sub = subs[i]
        next_sub = subs[i + 1]

        # 현재 자막의 종료 시간이 다음 자막의 시작 시간보다 늦으면 조정
        if current_sub.end > next_sub.start:
            # 다음 자막 시작 1ms 전으로 설정
            current_sub.end = pysrt.SubRipTime(
                milliseconds=next_sub.start.ordinal - 1
            )
            fixed_count += 1

    if fixed_count > 0:
        print(f"✓ {fixed_count}개의 겹치는 자막 타임스탬프를 수정했습니다.")
    else:
        print("✓ 겹치는 자막이 없습니다.")

    return subs


def remove_short_duplicates(subs, min_duration_ms=150):
    """
    150ms 미만의 짧고 중복된 자막을 제거합니다.

    Args:
        subs (SubRipFile): 자막 객체
        min_duration_ms (int): 최소 자막 지속 시간 (밀리초)

    Returns:
        SubRipFile: 정리된 자막 객체
    """
    filtered_subs = pysrt.SubRipFile()
    prev_text = None
    removed_count = 0

    for sub in subs:
        duration = sub.end.ordinal - sub.start.ordinal

        # 150ms 미만이고 이전 자막과 동일한 텍스트면 제거
        if duration < min_duration_ms and sub.text == prev_text:
            removed_count += 1
            continue

        filtered_subs.append(sub)
        prev_text = sub.text

    if removed_count > 0:
        print(f"✓ {removed_count}개의 짧은 중복 자막을 제거했습니다.")

    return filtered_subs


def group_subtitles(subs, max_gap_ms=300, max_len=150):
    """
    연속된 자막을 문맥을 고려하여 문장 단위로 합칩니다.

    Args:
        subs (SubRipFile): 자막 객체
        max_gap_ms (int): 자막을 합칠 최대 시간 간격 (밀리초)
        max_len (int): 합쳐진 자막의 최대 길이

    Returns:
        SubRipFile: 문장 단위로 합쳐진 자막 객체
    """
    if not subs:
        return subs

    grouped_subs = pysrt.SubRipFile()
    current_group = subs[0]
    # 첫 자막의 줄바꿈을 공백으로 변경
    current_group.text = current_group.text.replace('\n', ' ').strip()

    for i in range(1, len(subs)):
        next_sub = subs[i]
        gap = next_sub.start.ordinal - current_group.end.ordinal
        
        # 다음 자막 텍스트도 미리 정제
        next_text = next_sub.text.replace('\n', ' ').strip()

        # 조건: 시간 간격이 짧고, 합쳐도 길이가 너무 길지 않고, 현재 자막이 문장 끝이 아닐 때
        if (gap < max_gap_ms and
                len(current_group.text + ' ' + next_text) < max_len and
                not current_group.text.endswith(('.', '?', '!'))):
            
            # 자막 합치기
            current_group.text += ' ' + next_text
            current_group.end = next_sub.end
        else:
            # 현재 그룹을 리스트에 추가하고 새 그룹 시작
            grouped_subs.append(current_group)
            current_group = next_sub
            current_group.text = next_text # 새 그룹의 텍스트도 정제된 상태로 시작

    # 마지막 그룹 추가
    grouped_subs.append(current_group)

    merged_count = len(subs) - len(grouped_subs)
    if merged_count > 0:
        print(f"✓ {merged_count}개의 자막을 문장 단위로 병합했습니다.")

    return grouped_subs


def load_subtitle(subtitle_path):
    """
    자막 파일을 로드하고 겹침 및 문장 단위 병합을 자동으로 수행합니다.

    Args:
        subtitle_path (str): 자막 파일 경로

    Returns:
        SubRipFile: 파싱 및 처리된 자막 객체
    """
    if not os.path.exists(subtitle_path):
        raise FileNotFoundError(f"자막 파일을 찾을 수 없습니다: {subtitle_path}")

    print(f"자막 로드 중: {subtitle_path}")
    subs = pysrt.open(subtitle_path)
    print(f"총 {len(subs)}개의 자막 항목을 로드했습니다.")

    # 자막 전처리
    print("\n자막 전처리 중...")
    subs = fix_overlapping_subtitles(subs)
    subs = remove_short_duplicates(subs)
    subs = group_subtitles(subs) # 문장 단위 병합

    return subs


def save_subtitle(subs, output_path):
    """
    자막을 파일로 저장합니다.

    Args:
        subs (SubRipFile): 자막 객체
        output_path (str): 저장할 파일 경로
    """
    subs.save(output_path, encoding='utf-8')
    print(f"자막 저장 완료: {output_path}")


def get_subtitle_text(subs):
    """
    자막에서 모든 텍스트를 추출합니다.
    여러 줄로 된 자막을 한 줄로 합칩니다.

    Args:
        subs (SubRipFile): 자막 객체

    Returns:
        list: 자막 텍스트 리스트
    """
    # 줄바꿈을 공백으로 변경하여 한 줄로 만듦
    return [sub.text.replace('\n', ' ').strip() for sub in subs]


def update_subtitle_text(subs, translated_texts):
    """
    자막 텍스트를 번역된 텍스트로 업데이트합니다.

    Args:
        subs (SubRipFile): 자막 객체
        translated_texts (list): 번역된 텍스트 리스트

    Returns:
        SubRipFile: 업데이트된 자막 객체
    """
    if len(subs) != len(translated_texts):
        raise ValueError(f"자막 개수({len(subs)})와 번역된 텍스트 개수({len(translated_texts)})가 일치하지 않습니다.")

    for i, translated_text in enumerate(translated_texts):
        subs[i].text = translated_text

    print(f"{len(subs)}개의 자막을 업데이트했습니다.")
    return subs


if __name__ == "__main__":
    # 테스트
    pass
