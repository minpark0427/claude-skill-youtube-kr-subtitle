"""번역 모듈"""
from deep_translator import GoogleTranslator
import time
import re


def clean_text(text):
    """
    번역 전 텍스트를 정제합니다.

    Args:
        text (str): 원본 텍스트

    Returns:
        str: 정제된 텍스트
    """
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    text = text.strip()
    return text


def translate_texts(texts, source='en', target='ko', batch_size=50):
    """
    텍스트 리스트를 번역합니다.

    Args:
        texts (list): 번역할 텍스트 리스트
        source (str): 원본 언어 코드 (기본값: 'en')
        target (str): 목표 언어 코드 (기본값: 'ko')
        batch_size (int): 한 번에 처리할 텍스트 개수

    Returns:
        list: 번역된 텍스트 리스트
    """
    translator = GoogleTranslator(source=source, target=target)
    translated_texts = []

    print(f"총 {len(texts)}개의 문장을 번역합니다...")
    print("고품질 번역을 위해 시간이 다소 걸릴 수 있습니다...")

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        print(f"진행 중: {i + 1}/{len(texts)}")

        for idx, text in enumerate(batch):
            try:
                # 빈 텍스트는 그대로 유지
                if not text.strip():
                    translated_texts.append(text)
                    continue

                # 텍스트 정제
                cleaned_text = clean_text(text)

                # 번역 실행 (재시도 로직 포함)
                max_retries = 3
                for retry in range(max_retries):
                    try:
                        translated = translator.translate(cleaned_text)
                        if translated:
                            translated_texts.append(translated)
                            break
                    except Exception as retry_error:
                        if retry == max_retries - 1:
                            raise retry_error
                        time.sleep(0.5)
                else:
                    # 번역 실패 시 원본 사용
                    translated_texts.append(cleaned_text)

                # API 호출 제한을 피하기 위한 대기 (더 안정적인 번역)
                time.sleep(0.2)

            except Exception as e:
                print(f"번역 실패 (항목 {i + idx}): {e}")
                # 번역 실패 시 원본 텍스트 사용
                translated_texts.append(clean_text(text))

    print("번역 완료!")
    return translated_texts


def translate_subtitle_file(input_path, output_path, source='en', target='ko'):
    """
    자막 파일을 번역합니다.

    Args:
        input_path (str): 입력 자막 파일 경로
        output_path (str): 출력 자막 파일 경로
        source (str): 원본 언어 코드
        target (str): 목표 언어 코드
    """
    from subtitle_processor import load_subtitle, get_subtitle_text, update_subtitle_text, save_subtitle

    # 자막 로드
    subs = load_subtitle(input_path)

    # 자막 텍스트 추출
    texts = get_subtitle_text(subs)

    # 번역
    translated_texts = translate_texts(texts, source=source, target=target)

    # 자막 업데이트
    updated_subs = update_subtitle_text(subs, translated_texts)

    # 저장
    save_subtitle(updated_subs, output_path)


if __name__ == "__main__":
    # 테스트
    test_texts = ["Hello", "How are you?", "This is a test."]
    result = translate_texts(test_texts)
    print(result)
