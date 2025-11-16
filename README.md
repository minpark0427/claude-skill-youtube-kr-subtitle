# YouTube Korean Subtitle Auto-Insertion Service

YouTube 비디오에 한글 자막을 자동으로 삽입하는 Claude Code Skill입니다. Claude가 YouTube 비디오를 다운로드하고, 영어 자막을 추출하여 한글로 번역한 후, FFmpeg을 사용하여 비디오에 자막을 burn-in합니다.

## Claude Code Skill

이 레포지토리는 **Claude Code Skill**로 설계되었습니다. Clone하면 바로 사용 가능합니다!

### 빠른 시작

1. 이 레포지토리를 clone합니다:
   ```bash
   git clone <repository-url>
   cd auto_bzcf
   ```

2. 필수 요구사항을 설치합니다 (아래 참조)

3. Claude Code에서 프로젝트를 열고 요청합니다:
   ```
   "이 유튜브 영상에 한글 자막 넣어줘: https://youtube.com/watch?v=..."
   ```

4. Claude가 자동으로 전체 워크플로우를 실행합니다!

## 주요 기능

- YouTube 비디오 및 영어 자막 자동 다운로드
- Claude의 컨텍스트 기반 한글 번역 (비디오 메타데이터 + 웹 검색)
- YouTube 자막의 오버랩 타임스탬프 자동 수정
- 짧은 중복 자막 제거 및 문장 단위 그룹핑
- FFmpeg을 사용한 한글 자막 비디오 burn-in

## 필수 요구사항

### 시스템 요구사항
- Python 3.7 이상
- FFmpeg

### Python 패키지
```bash
pip install -r requirements.txt
```

주요 패키지:
- `yt-dlp` - YouTube 비디오 다운로드
- `pysrt` - SRT 자막 파일 처리

### FFmpeg 설치

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

## 디렉토리 구조

```
auto_bzcf/
├── .claude/
│   └── skills/
│       └── youtube-kr-subtitle/    # Claude Code Skill
│           ├── SKILL.md            # Skill 정의 및 워크플로우
│           └── scripts/            # 처리 스크립트들
│               ├── download_youtube.py
│               ├── extract_subtitle_text.py
│               ├── merge_translated_subtitle.py
│               └── process_video.py
├── downloads/            # 다운로드된 비디오 및 원본 자막 (임시)
├── output/              # 최종 처리된 비디오 (한글 자막 포함)
├── venv/                # Python 가상환경
└── README.md
```

## 사용 방법

### 스크립트 기반 워크플로우 (권장)

#### 1단계: 비디오 및 영어 자막 다운로드

```bash
python scripts/download_youtube.py "<youtube_url>" downloads/
```

**출력 예시:**
```json
{
  "video_path": "downloads/VideoTitle.mp4",
  "subtitle_path": "downloads/VideoTitle.en.srt",
  "title": "Video Title",
  "description": "Video description...",
  "duration": 1659,
  "video_id": "deMrq2uzRKA"
}
```

#### 2단계: 자막 텍스트 추출

```bash
python scripts/extract_subtitle_text.py downloads/VideoTitle.en.srt > subtitle_texts.json
```

**출력 예시:**
```json
{
  "texts": [
    "첫 번째 자막 텍스트",
    "두 번째 자막 텍스트"
  ],
  "metadata": {
    "total_count": 809,
    "processed_count": 235
  }
}
```

이 스크립트는 자동으로:
- YouTube의 오버랩 타임스탬프 수정
- 150ms 이하의 짧은 중복 자막 제거
- 연속된 자막을 문장 단위로 그룹핑 (최대 300ms 간격, 150자 이하)

#### 3단계: 한글로 번역

추출된 `texts` 배열을 한글로 번역하여 JSON 파일로 저장합니다.

**번역된 텍스트 예시 (translated_texts.json):**
```json
[
  "첫 번째 번역된 자막",
  "두 번째 번역된 자막"
]
```

**중요:** 번역된 배열의 길이는 원본 자막 개수와 정확히 일치해야 합니다.

#### 4단계: 번역된 텍스트와 타임스탬프 병합

```bash
python scripts/merge_translated_subtitle.py \
  downloads/VideoTitle.en.srt \
  translated_texts.json \
  downloads/VideoTitle.ko.srt
```

**출력 예시:**
```json
{
  "success": true,
  "subtitle_count": 235,
  "output_path": "downloads/VideoTitle.ko.srt"
}
```

#### 5단계: 비디오에 한글 자막 burn-in

```bash
python scripts/process_video.py \
  downloads/VideoTitle.mp4 \
  downloads/VideoTitle.ko.srt \
  output/VideoTitle_korean.mp4 \
  Arial 24
```

**매개변수:**
- `video_path`: 원본 비디오 파일 경로
- `subtitle_path`: 한글 SRT 파일 경로
- `output_path`: 출력 비디오 파일 경로
- `font_name`: 글꼴 이름 (선택사항, 기본값: Arial)
- `font_size`: 글꼴 크기 (선택사항, 기본값: 24)

**출력 예시:**
```json
{
  "success": true,
  "output_path": "output/VideoTitle_korean.mp4",
  "file_size_mb": 311.22
}
```

### 전체 워크플로우 예시

```bash
# 1. 비디오 다운로드
python scripts/download_youtube.py "https://www.youtube.com/watch?v=VIDEO_ID" downloads/

# 2. 자막 텍스트 추출
python scripts/extract_subtitle_text.py downloads/VideoTitle.en.srt > subtitle_texts.json

# 3. 번역 (수동 또는 번역 API 사용)
# subtitle_texts.json의 texts를 번역하여 translated_texts.json 생성

# 4. 번역과 타임스탬프 병합
python scripts/merge_translated_subtitle.py \
  downloads/VideoTitle.en.srt \
  translated_texts.json \
  downloads/VideoTitle.ko.srt

# 5. 비디오에 자막 burn-in
python scripts/process_video.py \
  downloads/VideoTitle.mp4 \
  downloads/VideoTitle.ko.srt \
  output/VideoTitle_korean.mp4
```

### 실제 사용 예시

```bash
# Michael Truell Cursor 인터뷰 비디오
python scripts/download_youtube.py "https://www.youtube.com/watch?v=deMrq2uzRKA" downloads/

python scripts/extract_subtitle_text.py "downloads/Michael Truell： How Cursor Builds at the Speed of AI.en.srt" > downloads/subtitle_texts.json

# 번역 후...

python scripts/merge_translated_subtitle.py \
  "downloads/Michael Truell： How Cursor Builds at the Speed of AI.en.srt" \
  downloads/translated_texts.json \
  "downloads/Michael Truell How Cursor Builds at the Speed of AI.ko.srt"

python scripts/process_video.py \
  "downloads/Michael Truell： How Cursor Builds at the Speed of AI.mp4" \
  "downloads/Michael Truell How Cursor Builds at the Speed of AI.ko.srt" \
  "output/Michael_Truell_Cursor_korean_$(date +%Y%m%d_%H%M%S).mp4" \
  Arial 20
```

## 스크립트 상세 설명

### download_youtube.py
YouTube 비디오와 영어 자막을 다운로드합니다.

**사용법:**
```bash
python scripts/download_youtube.py "<youtube_url>" <output_dir>
```

**출력:** 비디오 메타데이터 JSON (title, description, duration, video_id 등)

### extract_subtitle_text.py
SRT 파일을 전처리하고 번역할 텍스트 배열을 추출합니다.

**사용법:**
```bash
python scripts/extract_subtitle_text.py <subtitle_path>
```

**자동 처리:**
- YouTube의 오버랩 타임스탬프 수정
- 짧은 중복 자막 제거
- 문장 단위 그룹핑

**출력:** texts 배열과 메타데이터를 포함한 JSON

### merge_translated_subtitle.py
번역된 텍스트를 원본 SRT의 타임스탬프와 병합하여 한글 SRT 파일을 생성합니다.

**사용법:**
```bash
python scripts/merge_translated_subtitle.py <original_srt> <translated_json> <output_srt>
```

**중요:** 번역된 텍스트 개수는 원본 자막 개수와 정확히 일치해야 합니다.

### process_video.py
FFmpeg을 사용하여 한글 자막을 비디오에 burn-in합니다.

**사용법:**
```bash
python scripts/process_video.py <video_path> <subtitle_path> <output_path> [font_name] [font_size]
```

**자막 스타일:**
- 흰색 텍스트 (&HFFFFFF)
- 검은색 외곽선 (&H000000)
- 반투명 검은색 배경 (&H80000000)
- 외곽선 두께: 2
- 하단 여백: 20

## 주의사항

### YouTube 자막 오버랩 문제
YouTube 자동 생성 자막은 롤링 캡션 형식으로 의도적으로 타임스탬프가 겹칩니다. `extract_subtitle_text.py`가 이를 자동으로 수정합니다.

### 현재 제한사항
- 영어 자막이 있는 비디오만 처리 가능 (자동 생성 또는 수동)
- 자막이 없는 비디오는 현재 버전에서 지원하지 않음
- 긴 비디오의 경우 FFmpeg 처리에 시간이 걸릴 수 있음

### FFmpeg 경로 처리
`process_video.py`는 Windows 경로와 특수 문자를 처리하기 위한 특별한 경로 이스케이핑 로직을 포함합니다.

## 트러블슈팅

### FFmpeg을 찾을 수 없음
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### 자막 개수 불일치 오류
번역된 텍스트 배열의 길이가 원본 자막 개수와 일치하는지 확인하세요:
```bash
# 원본 자막 개수 확인
cat subtitle_texts.json | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'Count: {len(data[\"texts\"])}')"

# 번역본 개수 확인
cat translated_texts.json | python3 -c "import sys, json; data = json.load(sys.stdin); print(f'Count: {len(data)}')"
```

### 가상환경 활성화
항상 가상환경 내에서 작업하세요:
```bash
# 가상환경 생성
python3 -m venv venv

# 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 라이선스

이 프로젝트는 교육 및 공익 목적으로 제공됩니다.

## 면책 조항

원본 비디오의 저작권은 원저작권자에게 있습니다. YouTube 시스템을 통해 저작권 허가를 확인하며, 시스템 내 미확인 시 별도 이메일로 허가를 구합니다.

본 도구의 목적은 교육, 동기부여, 아이디어 공유 등 공익 목적이며, YouTube 수익은 전혀 발생하지 않습니다.

삭제, 수정 등 요청사항이 있으시면 문의해주시기 바랍니다.
