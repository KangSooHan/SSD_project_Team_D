import os
import shutil

import pytest
from shell_core.logger import Logger, LOG_FOLDER, CURRENT_LOG, MAX_LOG_SIZE

@pytest.fixture(autouse=True)
def clean_logs():
    # 로그 테스트 전후로 로그 폴더를 클리어
    if LOG_FOLDER.exists():
        shutil.rmtree(LOG_FOLDER)
    LOG_FOLDER.mkdir(exist_ok=True)
    yield
    shutil.rmtree(LOG_FOLDER)
    LOG_FOLDER.mkdir(exist_ok=True)

def test_로그파일에_쓰기_테스트():
    logger = Logger(show_console=False)
    logger.print("Test message")
    assert CURRENT_LOG.exists()
    with open(CURRENT_LOG, encoding="utf-8") as f:
        content = f.read()
    assert "Test message" in content

def test_로그파일에_여러개_쓰기_테스트():
    logger = Logger(show_console=False)
    logger.print("First message")
    logger.print("Second message")
    with open(CURRENT_LOG, encoding="utf-8") as f:
        content = f.read()
    assert "First message" in content
    assert "Second message" in content

def test_롤링테스트():
    logger = Logger(show_console=False)
    message = "A" * 200  # 각 라인 200 bytes

    for _ in range((MAX_LOG_SIZE // (len(message) + 40)) + 10):
        logger.print(message)
    rolled_logs = list(LOG_FOLDER.glob("until_*.log"))
    assert len(rolled_logs) >= 1
    assert CURRENT_LOG.exists()
    with open(CURRENT_LOG, encoding="utf-8") as f:
        assert message in f.read()

def test_오래된_로그를_zip으로_바꾸는지_체크():
    logger = Logger(show_console=False)
    message = "B" * 200
    # 2개 이상의 롤링 로그를 만들기 위해 충분히 많은 로그를 남김
    for _ in range(2 * ((MAX_LOG_SIZE // (len(message) + 40)) + 10)):
        logger.print(message)
    # 롤링된 로그가 2개 이상이면, 가장 오래된 로그가 .zip으로 변경되어야 함
    zipped = list(LOG_FOLDER.glob("*.zip"))
    assert len(zipped) == 1
    # .zip 파일 내용이 원래 로그 내용과 일치하는지 확인
    with open(zipped[0], encoding="utf-8") as f:
        assert message in f.read()
