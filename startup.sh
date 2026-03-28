#!/bin/bash

echo "ContentHub starting..."
echo "========================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "[错误] 未检测到Python，请先安装 Python 3.8+"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# 安装依赖
echo ""
echo "[1/2] 正在安装依赖..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败"
    exit 1
fi

# 启动服务
echo ""
echo "[2/2] 正在启动 ContentHub..."
echo "========================"
echo ""
echo "访问 http://localhost:8000/docs 查看API文档"
echo "按 Ctrl+C 停止服务"
echo ""

$PYTHON_CMD main.py
