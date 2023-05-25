@echo off
REM ตรวจสอบว่า Python ถูกติดตั้งแล้วหรือไม่
python --version
if %errorlevel% neq 0 (
    echo Python is not installed.
    pause
    exit /b
)

REM เปลี่ยน directory เข้าสู่โฟลเดอร์ที่มีไฟล์ app.py
cd /d D:\My_Project\udbot from Link

REM เรียกใช้ activate.bat เพื่อเปิดเครื่องมือเสริม
call env\Scripts\activate.bat

REM เรียกใช้ไฟล์ app.py
python app.py

pause