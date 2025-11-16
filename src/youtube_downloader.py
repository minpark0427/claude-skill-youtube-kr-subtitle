"""YouTube 영상 다운로드 모듈"""
import os
import yt_dlp


def download_video(url, output_dir="downloads"):
    """
    YouTube 영상을 다운로드합니다.

    Args:
        url (str): YouTube 영상 URL
        output_dir (str): 다운로드할 디렉토리

    Returns:
        dict: 다운로드된 파일 정보
    """
    # 출력 디렉토리가 없으면 생성
    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp 옵션 설정
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': False,
    }

    print(f"영상 다운로드 시작: {url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # 영상 정보 추출
        info = ydl.extract_info(url, download=True)

        # 다운로드된 파일 경로
        video_path = ydl.prepare_filename(info)

        return {
            'video_path': video_path,
            'title': info.get('title', 'Unknown'),
            'duration': info.get('duration', 0),
            'video_id': info.get('id', '')
        }


def download_subtitles(url, output_dir="downloads"):
    """
    YouTube 영상의 자막을 다운로드합니다.

    Args:
        url (str): YouTube 영상 URL
        output_dir (str): 다운로드할 디렉토리

    Returns:
        str: 다운로드된 자막 파일 경로 (없으면 None)
    """
    os.makedirs(output_dir, exist_ok=True)

    # 자막 다운로드 옵션
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'en-US', 'en-GB'],  # 영어 자막 우선
        'subtitlesformat': 'srt',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,
    }

    print("자막 다운로드 시도 중...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            # 다운로드된 자막 파일 찾기
            base_filename = ydl.prepare_filename(info)
            base_filename = os.path.splitext(base_filename)[0]

            # 가능한 자막 파일 경로들
            possible_subtitle_files = [
                f"{base_filename}.en.srt",
                f"{base_filename}.en-US.srt",
                f"{base_filename}.en-GB.srt",
            ]

            for subtitle_file in possible_subtitle_files:
                if os.path.exists(subtitle_file):
                    print(f"자막 파일 발견: {subtitle_file}")
                    return subtitle_file

            print("자막 파일을 찾을 수 없습니다.")
            return None

    except Exception as e:
        print(f"자막 다운로드 실패: {e}")
        return None


if __name__ == "__main__":
    # 테스트
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = download_video(test_url)
    print(f"다운로드 완료: {result}")
