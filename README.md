# YouTube 한글 자막 자동 삽입 서비스

YouTube 영상에 한글 자막을 자동으로 삽입하여 새로운 영상을 생성하는 프로그램입니다.

## 주요 기능

1. YouTube 영상 자동 다운로드
2. 영어 자막 자동 추출
3. **자막 타임스탬프 겹침 자동 수정** (YouTube 자막 특유의 문제 해결)
4. Google Translate를 이용한 한글 번역
5. FFmpeg를 이용한 자막 하드코딩 (영상에 직접 삽입)
6. 한 번에 하나의 자막만 깔끔하게 표시

## 실행 결과

입력: `https://www.youtube.com/watch?v=CBneTpXF1CQ`

출력: 한글 자막이 삽입된 MP4 파일
- 파일 크기: 약 23MB
- 127개의 자막 항목이 번역되어 삽입됨
- 출력 위치: `output/` 디렉토리

## 설치 방법

### 1. FFmpeg 설치

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# https://ffmpeg.org/download.html 에서 다운로드
```

### 2. Python 가상환경 생성 및 패키지 설치

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate     # Windows

# 패키지 설치
pip install -r requirements.txt
```

## 사용 방법

### 기본 사용법

```bash
# 가상환경 활성화
source venv/bin/activate

# 프로그램 실행
python main.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

### 예시

```bash
python main.py "https://www.youtube.com/watch?v=CBneTpXF1CQ"
```

## 프로젝트 구조

```
auto_bzcf/
├── src/
│   ├── __init__.py
│   ├── youtube_downloader.py    # YouTube 다운로드 모듈
│   ├── subtitle_processor.py     # 자막 처리 모듈
│   ├── translator.py             # 번역 모듈
│   └── video_processor.py        # 영상 처리 및 자막 삽입 모듈
├── downloads/                    # 다운로드된 파일 저장
├── output/                       # 최종 결과물 저장
├── main.py                       # 메인 실행 스크립트
├── requirements.txt              # 필요한 패키지 목록
├── PLAN.md                       # 프로젝트 계획서
└── README.md                     # 이 파일
```

## 처리 과정

1. **영상 다운로드**: yt-dlp를 사용하여 YouTube 영상 다운로드
2. **자막 다운로드**: 영상에서 영어 자막 추출
3. **자막 타임스탬프 수정**:
   - YouTube 자막은 2줄 롤링 캡션 스타일로 타임스탬프가 겹침
   - 자동으로 겹침을 감지하고 수정 (각 자막이 다음 자막 시작 1ms 전에 종료)
   - 150ms 미만의 짧은 중복 자막 자동 제거
4. **한글 번역**: Google Translate를 통해 자막을 한글로 번역
5. **자막 삽입**: FFmpeg를 사용하여 영상에 자막 하드코딩
6. **결과 저장**: `output/` 디렉토리에 최종 영상 저장

## 필요한 패키지

- `yt-dlp`: YouTube 다운로더
- `ffmpeg-python`: 영상 처리
- `deep-translator`: 번역 (Google Translate)
- `pysrt`: 자막 파일 파싱

## 제한사항

- 영어 자막이 있는 YouTube 영상만 처리 가능
- 자막이 없는 영상은 현재 버전에서는 지원하지 않음 (Phase 1에서 Whisper STT 추가 예정)
- 번역 품질은 Google Translate의 성능에 의존

## 향후 개선 사항 (Phase 1)

1. Whisper STT 통합 (자막이 없는 영상 지원)
2. GPT 번역 옵션 추가 (더 높은 번역 품질)
3. 자막 스타일 커스터마이징 (폰트, 색상, 위치)
4. 웹 UI 구축

## 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다. YouTube 이용약관을 준수하여 사용하시기 바랍니다.

## 문제 해결

### "FFmpeg가 설치되어 있지 않습니다" 오류

FFmpeg를 먼저 설치해주세요:
```bash
brew install ffmpeg  # macOS
```

### "자막을 다운로드할 수 없습니다" 오류

해당 YouTube 영상에 영어 자막이 없는 경우입니다. 자막이 있는 다른 영상을 시도하거나, Phase 1에서 추가될 Whisper STT 기능을 기다려주세요.

### 번역이 느린 경우

Google Translate API 호출 제한으로 인해 각 자막 사이에 0.2초의 대기 시간이 있습니다. 긴 영상의 경우 시간이 더 걸릴 수 있습니다.

### 자막 겹침 문제

**이 문제는 자동으로 해결됩니다!**

YouTube 자동 생성 자막은 2줄 롤링 캡션 스타일을 사용하여 타임스탬프가 의도적으로 겹칩니다. 프로그램이 자동으로:
- 겹치는 타임스탬프를 감지 및 수정
- 각 자막의 종료 시간을 다음 자막 시작 1ms 전으로 조정
- 짧은 중복 자막 제거

웹 검색을 통해 찾은 업계 표준 알고리즘을 적용하여 한 번에 하나의 자막만 깔끔하게 표시됩니다.
