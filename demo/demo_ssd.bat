@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

rem 함수 선언부는 스크립트 맨 아래에 배치할 예정이니, 먼저 main으로 이동
goto :main

:print_files
setlocal enabledelayedexpansion
set "DIRNAME=%~1"
set "FILELIST="

for %%f in ("%DIRNAME%\*") do (
    set "FILELIST=!FILELIST!%%~nxf, "
)

if defined FILELIST (
    set "FILELIST=%FILELIST:~0,-2%"
) else (
    set "FILELIST=폴더가 비어있음"
)

echo %DIRNAME% 폴더 파일: %FILELIST%

endlocal
goto :eof

:print_ssd_nand
setlocal enabledelayedexpansion

set "CONTENT="

if not exist ssd_nand.txt (
    echo ssd_nand.txt 파일이 존재하지 않습니다.
    endlocal
    goto :eof
)

for /f "usebackq delims=" %%L in ("ssd_nand.txt") do (
    set "LINE=%%L"
    if defined CONTENT (
        set "CONTENT=!CONTENT!,!LINE!"
    ) else (
        set "CONTENT=!LINE!"
    )
)

echo ssd_nand.txt 내용 (쉼표 구분):
echo !CONTENT!

endlocal
goto :eof

:main
rmdir /s /q buffer
if exist ssd_nand.txt del /f /q ssd_nand.txt
echo ==== SSD 시연 시작 ====
echo.

cls
echo [1] 기본 Write 검증
echo 실행: python ssd.py W 3 0x00000003
python ssd.py W 3 0x00000003
echo.
echo [Buffer 상태]
call :print_files buffer
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [2] Read 검증
echo 실행: python ssd.py R 3
python ssd.py R 3
echo.
echo [ssd_output.txt 상태](type ssd_output.txt)
type ssd_output.txt
echo.
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [3] 연속 Write (Flush 테스트용)
echo 실행: python ssd.py W 4 0x00000004
python ssd.py W 4 0x00000004
call :print_files buffer

echo.
echo 실행: python ssd.py W 5 0x00000005
python ssd.py W 5 0x00000005
call :print_files buffer

echo.
echo 실행: python ssd.py W 6 0x00000006
python ssd.py W 6 0x00000006
call :print_files buffer

echo.
echo 실행: python ssd.py W 7 0x00000007
python ssd.py W 7 0x00000007
call :print_files buffer

echo.
echo 실행: python ssd.py W 8 0x00000008
python ssd.py W 8 0x00000008
call :print_files buffer

echo.
echo 실행: python ssd.py R 7
python ssd.py R 7
echo [ssd_output.txt 상태](type ssd_output.txt)
type ssd_output.txt
echo.

echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.

echo [4] Fast Read Write 테스트
echo 실행: python ssd.py R 8
python ssd.py R 8
echo [ssd_output.txt 상태](type ssd_output.txt)
type ssd_output.txt
echo.

echo.
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [5] Flush 테스트
echo.
echo [Buffer 상태]
call :print_files buffer
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
echo 실행: python ssd.py F
python ssd.py F
echo.
echo [Buffer 상태]
call :print_files buffer
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [6] Ignore Command 테스트
echo 실행: python ssd.py W 9 0x00000009
python ssd.py W 9 0x00000009
echo.
echo [Buffer 상태]
call :print_files buffer
echo.
echo 실행: python ssd.py E 8 5
python ssd.py E 8 5
echo.
echo [Buffer 상태]
call :print_files buffer
echo 다음 테스트로 넘어가려면 Enter를 누르세요...
pause > nul

cls
echo [7] Erase + Merge Command 테스트
echo.
echo [Buffer 상태]
call :print_files buffer
echo.
echo 실행: python ssd.py E 10 6
python ssd.py E 10 6
echo.
echo [Buffer 상태]
call :print_files buffer

echo ==== SSD 시연 종료 ====
pause > nul
