@echo off
chcp 65001 > nul
setlocal

cls
echo ===============================
echo       [Runner 시연 시작]
echo ===============================
echo.

echo [1] python shell.py 실행 (인터랙티브 모드)
echo -----------------------------------------------
echo 이 모드는 사용자가 직접 명령어를 입력하는 방식입니다.
echo 종료하려면 exit 또는 Ctrl+C를 사용하세요.
pause
cls
python shell.py
echo.
echo [인터랙티브 모드 종료됨]
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [2] python shell.py shell_scripts.txt 실행
echo -----------------------------------------------
echo 사전 정의된 명령어가 들어 있는 shell_scripts.txt 파일을 실행합니다.
echo 실제 명령어 실행 결과를 확인해보세요.
pause
cls
python shell.py shell_scripts.txt
echo.
echo [스크립트 실행 완료]
echo.
pause > nul

echo ===============================
echo       [Runner 시연 종료]
echo ===============================
pause > nul