import os
import inspect
from datetime import datetime
from pathlib import Path

# ✅ 항상 프로젝트 루트 기준으로 logs/ 디렉토리를 생성
ROOT_DIR = Path(__file__).resolve().parent.parent
LOG_FOLDER = ROOT_DIR / "logs"
LOG_FOLDER.mkdir(exist_ok=True)

# 로그 파일 이름 설정
CURRENT_LOG = LOG_FOLDER / "latest.log"
MAX_LOG_SIZE = 10 * 1024  # 10KB


class Logger:
    def __init__(self, show_console: bool = False):
        """
        Logger 초기화
        :param show_console: True이면 콘솔에도 출력, False이면 파일에만 출력
        """
        self.show_console = show_console

    def _get_timestamp(self) -> str:
        """로그 출력용 현재 시간"""
        return datetime.now().strftime("%y.%m.%d %H:%M")

    def _get_filename_timestamp(self) -> str:
        """파일 이름용 현재 시간 (YYMMDD_HHMMSS)"""
        return datetime.now().strftime("%y%m%d_%Hh_%Mm_%Ss")

    def _get_calling_function(self) -> str:
        """
        logger.print를 호출한 함수명(class.method 또는 function)을 추출
        """
        stack = inspect.stack()
        caller = stack[2]  # 0: 현재 함수, 1: print, 2: 호출한 곳
        function_name = caller.function

        if 'self' in caller.frame.f_locals:
            class_name = caller.frame.f_locals['self'].__class__.__name__
            return f"{class_name}.{function_name}"
        else:
            return function_name

    def _check_and_roll_log(self):
        """latest.log가 10KB를 넘으면 이름 변경 후 롤링 처리"""
        if CURRENT_LOG.exists() and CURRENT_LOG.stat().st_size > MAX_LOG_SIZE:
            new_name = LOG_FOLDER / f"until_{self._get_filename_timestamp()}.log"
            CURRENT_LOG.rename(new_name)
            self._compress_old_logs()

    def _compress_old_logs(self):
        """
        롤링된 로그가 2개 이상이면
        가장 오래된 로그 파일을 .zip 확장자로 이름 변경
        (실제 압축은 하지 않음)
        """
        log_files = sorted(LOG_FOLDER.glob("until_*.log"), key=os.path.getmtime)
        if len(log_files) >= 2:
            oldest = log_files[0]
            zip_name = oldest.with_suffix(".zip")
            oldest.rename(zip_name)

    def print(self, message: str):
        """
        메시지를 로그로 출력 (파일에 저장하고, 필요 시 콘솔에도 출력)
        :param message: 로그로 출력할 메시지
        """
        self._check_and_roll_log()
        timestamp = self._get_timestamp()
        caller = self._get_calling_function()
        formatted_func = f"{caller}( )".ljust(30)
        log_message = f"[{timestamp}] {formatted_func}: {message}"

        if self.show_console:
            print(log_message)

        with open(CURRENT_LOG, "a", encoding="utf-8") as f:
            f.write(log_message + "\n")


# ✅ 전역 logger 인스턴스 (콘솔 출력 OFF가 기본값)
logger = Logger(show_console=False)
