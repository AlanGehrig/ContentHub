@echo off
echo ContentHub 启动中（端口 8001）...
echo ============================
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 安装依赖（如果需要）
echo.
echo 正在启动 ContentHub...
echo ============================
echo.
echo 访问 http://localhost:8001 查看前端页面
echo 访问 http://localhost:8001/docs 查看API文档
echo 按 Ctrl+C 停止服务
echo.

python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001, log_level='info')"

pause
