@echo off
cd /d "%~dp0"
echo Starting ContentHub on port 8001...
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8001, log_level='info')"
pause
