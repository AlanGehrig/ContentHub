@echo off
echo ContentHub 启动中...
echo ============================
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo [1/2] 正在安装依赖...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

REM 启动服务
echo.
echo [2/2] 正在启动 ContentHub...
echo ============================
echo.
echo 访问 http://localhost:8000/docs 查看API文档
echo 按 Ctrl+C 停止服务
echo.

python main.py

pause
