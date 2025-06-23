# 🔧 SSD Project Team D

Python으로 구현한 가상 SSD 시스템과 이를 검증하는 Test Shell, Test Script가 포함된 프로젝트입니다.

---

## 📘 개요

본 프로젝트는 하드웨어 SSD 없이 소프트웨어적으로 SSD의 Read/Write 동작을 시뮬레이션하며, 사용자가 입력한 명령을 파일 입출력 기반으로 처리합니다. 또한, 명령어 기반의 Shell 환경과 자동화된 Test Script를 통해 SSD 동작의 정확성과 일관성을 검증할 수 있도록 설계되었습니다.

---

## 📁 폴더 구조

```
SSD_project_Team_D/
├── .gitignore
├── README.md                     # 프로젝트 설명서
├── requirements.txt              # 필요한 Python 패키지 정의
├── shell.py                      # 메인 셸 인터페이스
├── shell_scripts.txt             # 셸 테스트 스크립트 예시
├── ssd.py                        # SSD 기능 실행 진입점
├── validator.py                  # 입력값 검증기
│
├── .github/
│   └── PULL_REQUEST_TEMPLATE.md  # PR 템플릿
│
├── command_core/                 # 명령어 실행 핵심 로직
│   ├── base_command.py           # 명령어 추상 클래스 (Command Pattern)
│   ├── command_factory.py        # 명령어 생성 및 매핑
│   ├── shell_commands/           # 실제 명령어 구현들
│   │   ├── erase_command.py
│   │   ├── erase_range_command.py
│   │   ├── exit_command.py
│   │   ├── flush_command.py
│   │   ├── full_read_command.py
│   │   ├── full_write_command.py
│   │   ├── help_command.py
│   │   ├── read_command.py
│   │   ├── write_command.py
│   │   ├── runner.py             # 명령어 실행 엔진
│   │   └── testscenario.py       # 시나리오 기반 테스트
│   └── utils/
│       └── erase_utils.py        # erase 관련 보조 함수
│
├── shell_core/                   # 셸-SSD 연동용 드라이버
│   ├── logger.py                 # 로그 출력 유틸
│   └── normal_ssd_driver.py      # SSD 드라이버 구현체
│
├── ssd_core/                     # SSD 동작과 관련된 핵심 모듈
│   ├── abstract_ssd.py           # SSD 인터페이스 정의
│   ├── abstract_ssd_driver.py    # SSD 드라이버 인터페이스
│   ├── abstract_buffer_optimizer.py  # 버퍼 최적화 인터페이스
│   ├── buffer.py                 # 내부 버퍼 구조
│   ├── discovery_buffer_optimizer.py
│   ├── simple_buffer_optimizer.py
│   ├── normal_ssd.py             # 실제 SSD 구현체
│   └── init.py                   # 초기화 함수들
│
├── tests/                        # TDD 기반 테스트 모듈
│   ├── test_buffer.py
│   ├── test_discovery_buffer_optimizer.py
│   ├── test_logger.py
│   ├── test_shell.py
│   ├── test_shell_erase.py
│   ├── test_shell_erase_range.py
│   ├── test_shell_exit_command.py
│   ├── test_shell_full_read_command.py
│   ├── test_shell_full_write_command.py
│   ├── test_shell_help_command.py
│   ├── test_shell_normal_ssd_driver.py
│   ├── test_shell_read.py
│   ├── test_shell_run.py
│   ├── test_shell_write_command.py
│   ├── test_ssd.py
│   ├── test_ssd_io.py
│   ├── test_testscenario1.py
│   ├── test_testscenario2.py
│   ├── test_testscenario3.py
│   ├── test_testscenario4.py
│   └── test_validator.py
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
  - `erase [LBA] [SIZE]`
  - `erase_range [START LBA] [END LBA]`

### 🔹 Test Script

- 자동화된 시나리오 기반 검증 도구
- 예시:
  - `1_FullWriteAndReadCompare`
  - `2_PartialLBAWrite`
  - `3_WriteReadAging`
  - `4_EraseAndWriteAging`
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

| 파일명                 | 역할                                 |
|---------------------|------------------------------------|
| `ssd_nand.txt`      | 모든 Write 결과가 저장되는 파일. LBA-값 형태로 기록 |
| `ssd_output.txt`    | 마지막 Read 결과가 저장되는 파일               |
| `ssd.py`            | 명령어 기반 실행 CLI 엔트리포인트               |
| `validator.py`      | 유저 입력값 검증기                         |
| `shell.py`          | 유저 입력 기반 명령 인터페이스                  |
| `shell_scripts.txt` | 기입된 Test Script들을 순차적으로 실행하는 기능    |

---

## 🧪 테스트 스크립트 구성 예시

### 1. FullWriteAndReadCompare
- 전 LBA에 write 후 read 값 비교
- 실패시 FAIL, 성공시 PASS 출력

### 2. PartialLBAWrite
- 순서를 섞어가며 특정 LBA에 반복 저장
- 마지막에 read 값 비교

### 3. WriteReadAging
- 0번과 99번 LBA에 200회 반복 write/read
- read 결과가 일치하는지 비교

### 4. EraseAndWriteAging
- 2,4,6 ~ 96번 LBA에 write 및 재 write 후 2~4, 4~6,...,96~98 LBA 삭제 30번 반복
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