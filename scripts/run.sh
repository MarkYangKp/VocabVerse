#!/bin/bash
set -e

# 定义颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 默认端口
WEB_PORT=9989

# 解析命令行参数
show_help() {
  echo "用法: $0 [选项...]" >&2
  echo
  echo "  -w, --web-port PORT    指定Web服务端口 (默认: 9989)"
  echo "  -h, --help             显示这个帮助信息"
  echo
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -w|--web-port)
      WEB_PORT="$2"
      shift 2
      ;;
    -h|--help)
      show_help
      exit 0
      ;;
    *)
      echo -e "${RED}未知参数: $1${NC}" >&2
      show_help
      exit 1
      ;;
  esac
done

echo -e "${YELLOW}使用端口配置: Web=${WEB_PORT}${NC}"

# 检查环境文件是否存在
echo "检查环境文件..."
if [ ! -f ".env-web-copy" ] || [ ! -f ".env-api-copy" ]; then
  echo -e "${RED}错误: 未找到环境文件!${NC}"
  exit 1
fi

echo -e "${GREEN}复制环境文件...${NC}"
cp .env-web-copy ../web/.env 
cp .env-api-copy ../api/.env

# 检查并移除已存在的容器
echo "检查是否有已存在的容器..."
if [ "$(docker ps -a -q -f name=vocabverse-web-container)" ]; then
  echo "移除旧的 web 容器..."
  docker rm -f vocabverse-web-container
fi

# 创建Docker网络（如果不存在）
if ! docker network inspect vocabverse-network >/dev/null 2>&1; then
  echo "创建Docker网络..."
  docker network create vocabverse-network
fi

echo -e "${GREEN}构建 web 镜像...${NC}"
docker build -t vocabverse-web -f ../web/Dockerfile ../web

echo -e "${GREEN}部署容器...${NC}"
docker run -d --name vocabverse-web-container --network vocabverse-network -p ${WEB_PORT}:80 vocabverse-web

# 检查容器是否成功启动
echo "检查容器状态..."
if [ "$(docker ps -q -f name=vocabverse-web-container)" ]; then
  echo -e "${GREEN}容器成功启动!${NC}"
else
  echo -e "${RED}错误: 容器启动失败!${NC}"
  docker logs vocabverse-web-container
  exit 1
fi

# 添加后端部署步骤
echo -e "${GREEN}部署后端...${NC}"
cd ../api  # 切换到后端目录
python3 -m venv venv       # 创建虚拟环境
source venv/bin/activate   # 激活虚拟环境
pip install -r requirements.txt  # 安装依赖
nohup python3 main.py &    # 后台启动后端服务

echo -e "${GREEN}部署完成!${NC}"
echo "API服务: http://localhost:9988"
