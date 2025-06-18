# 🔧 SSD Project Team D

Python으로 구현한 가상 SSD 시스템과 이를 검증하는 Test Shell, Test Script가 포함된 프로젝트입니다.

---

## 📘 개요

본 프로젝트는 하드웨어 SSD 없이 소프트웨어적으로 SSD의 Read/Write 동작을 시뮬레이션하며, 사용자가 입력한 명령을 파일 입출력 기반으로 처리합니다. 또한, 명령어 기반의 Shell 환경과 자동화된 Test Script를 통해 SSD 동작의 정확성과 일관성을 검증할 수 있도록 설계되었습니다.

---

## 📁 폴더 구조

```
SSD_project_Team_D/
├── ssd/                     # SSD 동작 로직 (read/write)
│   ├── abstract_ssd.py      # SSD 인터페이스 정의
│   ├── normal_ssd.py        # 기본 SSD 구현체
│
├── shell/                   # 테스트용 명령어 Shell
│   ├── commands/            # read, write 등 명령어 구현
│   └── shell.py             # 사용자 입력 처리 루프
│
├── tests/                   # pytest 기반 테스트 스크립트
│   └── test_ssd.py
│
├── .github/                 # PR 템플릿, 워크플로우 등
├── README.md                # 프로젝트 설명 문서
├── requirements.txt         # 의존성 목록
├── ssd.py                   # CLI 진입점 (Read/Write)
├── validator.py             # 명령어 및 파라미터 유효성 검사
├── ssd_nand.txt             # SSD 저장 파일 (자동 생성)
└── ssd_output.txt           # Read 결과 파일 (자동 생성)
```

---

## 🧠 배경 지식 요약

- SSD는 LBA (Logical Block Address) 단위로 데이터를 저장하며, 하나의 LBA는 **4 Byte**를 저장
- 본 프로젝트에서는 **LBA 0~99**까지 총 100칸을 가상으로 지원하여 **400 Byte 저장 공간**을 시뮬레이션
- 모든 저장은 `ssd_nand.txt` 파일에 이루어지며, 읽기 결과는 `ssd_output.txt`에 저장

---

## 🛠️ 주요 구성 요소 설명

### 🔹 SSD

- `AbstractSSD`: SSD의 기본 인터페이스 (read, write 정의)
- `NormalSSD`: 파일 기반으로 read/write 동작을 수행
- 읽기 시 존재하지 않는 LBA는 `0x00000000` 반환
- 유효하지 않은 명령은 `"ERROR"`를 `ssd_output.txt`에 기록

### 🔹 Shell

- 사용자 명령을 받아 CLI 방식으로 SSD를 테스트할 수 있도록 지원
- Shell에서 지원하는 명령어:
  - `read [LBA]`
  - `write [LBA] [VALUE]`
  - `fullread`
  - `fullwrite [VALUE]`
  - `help`
  - `exit`

### 🔹 Test Script

- 자동화된 시나리오 기반 검증 도구
- 예시:
  - `1_FullWriteAndReadCompare`
  - `2_PartialLBAWrite`
  - `3_WriteReadAging`
- 입력: `1_`, `2_` 등으로 실행 가능

---

## 🚀 설치 및 실행

```bash
# 1. 저장소 클론
git clone https://github.com/KangSooHan/SSD_project_Team_D.git
cd SSD_project_Team_D

# 2. 가상환경 설정 (옵션)
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 테스트 실행
pytest
```

---

## 🧪 예시 명령어 사용법

### ✅ Write

```bash
python ssd.py W 20 0x1289CDEF
```
- 20번 LBA에 0x1289CDEF 저장
- 출력 없음
- 내부적으로 `ssd_nand.txt`에 저장됨

### ✅ Read

```bash
python ssd.py R 20
```
- `ssd_output.txt`에 `0x1289CDEF` 저장됨
- 존재하지 않는 LBA는 `0x00000000`
- LBA 범위 오류 시 `"ERROR"` 출력

---

## 📂 파일 상세 설명

| 파일명 | 역할 |
|--------|------|
| `ssd_nand.txt` | 모든 Write 결과가 저장되는 파일. LBA-값 형태로 기록 |
| `ssd_output.txt` | 마지막 Read 결과가 저장되는 파일 |
| `ssd.py` | 명령어 기반 실행 CLI 엔트리포인트 |
| `test_ssd.py` | pytest 기반 SSD 기능 검증 테스트 코드 |
| `shell.py` | 유저 입력 기반 명령 인터페이스 |

---

## 🧪 테스트 스크립트 구성 예시

### 1. FullWriteAndReadCompare
```bash
> 1_
```
- 전 LBA에 write 후 read 값 비교
- 실패시 FAIL, 성공시 PASS 출력

### 2. PartialLBAWrite
- 순서를 섞어가며 특정 LBA에 반복 저장
- 마지막에 read 값 비교

### 3. WriteReadAging
- 0번과 99번 LBA에 200회 반복 write/read
- read 결과가 일치하는지 비교

---

## 🧑‍💻 팀 소개

- **팀명:** SSD Project Team D
- **참여자:** chiwona11, jiyoung61, winsowss, jihoonlee91, hkmilk0829, gbyl2024, changheum, KangSooHan

---

## 🗓️ 개발 및 발표 일정

| 일정 | 내용 |
|------|------|
| 1~2일차 | TDD 기반 SSD & Shell 개발<br>Test Double 사용 권장 |
| 3~4일차 | 명령어 추가, 리팩토링, 성능 개선 |
| 5일차 | 발표 준비 (PPT, 코드 캡처, 리팩토링 결과 등 포함) |