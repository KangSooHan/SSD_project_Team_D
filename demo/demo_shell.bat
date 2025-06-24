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

echo ===============================
echo        [Shell 시연 시작]
echo ===============================
echo.
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "INVALID_INPUT"
echo.
(
    echo write -1 0x11111111
    echo wrrite 1 0xAAAAAAAA
    echo write 5 0xFFFFFFFFF
    echo read 100
    echo flush 100
    echo erase -1 100
    echo erase_range -1 100
    echo 1_ 0xABCDEFGH
    echo exit
) > temp.txt
type temp.txt
python shell.py < temp.txt
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "help"
(
    echo help
    echo exit
) > temp.txt
python shell.py < temp.txt
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo [COMMAND] "write 0~6 & read 1,6,7"
echo 실행: "write & read"
(
    echo write 0 0x00000000
    echo write 1 0x00000001
    echo write 2 0x00000002
    echo write 3 0x00000003
    echo write 4 0x00000004
    echo write 5 0x00000005
    echo write 6 0x00000006
    echo read 1
    echo read 6
    echo read 7
    echo exit
) > temp.txt
python shell.py < temp.txt
echo.
echo [Buffer 상태]
call :print_files buffer
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
echo [ssd_output.txt 상태](type ssd_output.txt)
type ssd_output.txt
echo.
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "flush"
echo [Buffer 상태]
call :print_files buffer
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
(
    echo flush
    echo exit
) > temp.txt
python shell.py < temp.txt
echo.
echo.
echo [Buffer 상태]
call :print_files buffer
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.

echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "fullwrite"
echo.
(
    echo fullwrite 0xFFFFFFFF
    echo exit
) > temp.txt
python shell.py < temp.txt
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.

echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "fullread"
echo.
(
    echo fullread
    echo exit
) > temp.txt
python shell.py < temp.txt
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "erase 1 3 & erase 99 100 & erase 97 -5 & erase 0 -1 -> 0~3 93~97 99 제거"
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
(
    echo erase 1 3
    echo erase 99 100
    echo erase 97 -5
    echo erase 0 -1
    echo flush
    echo exit
) > temp.txt
python shell.py < temp.txt
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "erase_range 1 4 & erase_range 9 5 -> 0~9까지 제거"
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
(
    echo erase_range 1 4
    echo erase_range 9 5
    echo flush
    echo exit
) > temp.txt
python shell.py < temp.txt
echo.
echo [ssd_nand.txt 상태]
call :print_ssd_nand
echo.
echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo 실행: "Logger 검증"
echo.

(
    for /L %%i in (1,1,300) do (
        echo read 0
    )
    echo exit
) > temp.txt

python shell.py < temp.txt

echo 다음 명령어를 실행하려면 Enter 키를 누르세요...
pause > nul

cls
echo ===============================
echo        [Shell 시연 종료]
echo ===============================
del temp.txt > nul
pause
