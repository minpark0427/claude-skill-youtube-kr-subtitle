"""YouTube 한글 자막 자동 삽입 서비스 - 메인 스크립트"""
import os
import sys
from datetime import datetime

# src 디렉토리를 모듈 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from youtube_downloader import download_video, download_subtitles
from translator import translate_subtitle_file
from video_processor import burn_subtitles, check_ffmpeg


def main(youtube_url):
    """
    YouTube 영상에 한글 자막을 삽입하는 메인 프로세스

    Args:
        youtube_url (str): YouTube 영상 URL
    """
    print("=" * 60)
    print("YouTube 한글 자막 자동 삽입 서비스")
    print("=" * 60)
    print()

    # FFmpeg 확인
    if not check_ffmpeg():
        print("\n오류: FFmpeg가 설치되어 있지 않습니다.")
        print("macOS에서 설치: brew install ffmpeg")
        return

    try:
        # 1. 영상 다운로드
        print("\n[1/5] 영상 다운로드")
        print("-" * 60)
        video_info = download_video(youtube_url, output_dir="downloads")
        video_path = video_info['video_path']
        print(f"✓ 다운로드 완료: {video_info['title']}")

        # 2. 자막 다운로드
        print("\n[2/5] 자막 다운로드")
        print("-" * 60)
        subtitle_path = download_subtitles(youtube_url, output_dir="downloads")

        if not subtitle_path:
            print("\n오류: 자막을 다운로드할 수 없습니다.")
            print("이 영상에는 영어 자막이 없거나 자막을 사용할 수 없습니다.")
            print("\n해결 방법:")
            print("1. YouTube에서 자막이 제공되는 다른 영상을 선택하세요.")
            print("2. 또는 Whisper STT 기능을 구현하여 음성에서 자막을 생성하세요. (Phase 1)")
            return

        print(f"✓ 자막 다운로드 완료: {subtitle_path}")

        # 3. 한글 번역
        print("\n[3/5] 한글 번역")
        print("-" * 60)
        # 번역된 자막 파일 경로
        base_name = os.path.splitext(subtitle_path)[0]
        translated_subtitle_path = f"{base_name}.ko.srt"

        translate_subtitle_file(
            input_path=subtitle_path,
            output_path=translated_subtitle_path,
            source='en',
            target='ko'
        )
        print(f"✓ 번역 완료: {translated_subtitle_path}")

        # 4. 자막 삽입
        print("\n[4/5] 자막 삽입")
        print("-" * 60)
        # 출력 파일 경로
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{video_info['title']}_ko_{timestamp}.mp4"
        output_path = os.path.join("output", output_filename)

        burn_subtitles(
            video_path=video_path,
            subtitle_path=translated_subtitle_path,
            output_path=output_path,
            font_name="Arial",
            font_size=24
        )

        # 5. 완료
        print("\n[5/5] 완료")
        print("=" * 60)
        print(f"✓ 처리 완료!")
        print(f"✓ 출력 파일: {output_path}")
        print(f"✓ 파일 크기: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
        print("=" * 60)

    except Exception as e:
        print(f"\n오류 발생: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # 사용자가 제공한 YouTube URL
    url = "https://www.youtube.com/watch?v=CBneTpXF1CQ"

    if len(sys.argv) > 1:
        url = sys.argv[1]

    main(url)
