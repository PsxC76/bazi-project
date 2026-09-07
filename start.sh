#!/bin/bash
# 本地开发启动脚本

set -e

echo "=========================================="
echo "  八字命理案例库 - 本地开发环境"
echo "=========================================="
echo ""

# Check dependencies
echo "检查依赖..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3，请先安装"
    exit 1
fi

# Check Node
if ! command -v node &> /dev/null; then
    echo "错误: 未找到 Node.js，请先安装"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "警告: 未找到 PostgreSQL 客户端"
fi

echo ""
echo "1. 启动数据库 (Docker)..."
docker-compose up -d db redis

echo ""
echo "2. 安装后端依赖..."
cd backend
pip install -r requirements.txt -q

echo ""
echo "3. 启动后端服务..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

echo ""
echo "4. 安装前端依赖..."
cd frontend
npm install

echo ""
echo "5. 启动前端服务..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "  服务已启动！"
echo "=========================================="
echo ""
echo "  前端: http://localhost:3000"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "  按 Ctrl+C 停止所有服务"
echo ""

# Trap exit
trap "echo '停止服务...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker-compose down; exit" INT TERM

wait
