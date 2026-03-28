@echo off
echo 安装 ContentHub 依赖...
echo ============================
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖安装失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ============================
echo 安装完成！运行 startup.bat 启动 ContentHub
echo.
pause
