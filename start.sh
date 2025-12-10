#!/bin/bash

# ==========================================
# 1. 环境初始化与权限修正
# ==========================================

# 定义目录路径
EXCHANGE_DIR="/export/jupyterhub/exchange"
DATA_DIR="/export/jupyterhub/data"

# 确保目录存在 (如果删除了目录，这里会自动重建)
mkdir -p "$EXCHANGE_DIR"
mkdir -p "$DATA_DIR"

echo "正在初始化..."

chmod 777 "$EXCHANGE_DIR"
chown 1000:100 "$EXCHANGE_DIR"
chown -R 1000:100 "$DATA_DIR"

# ==========================================
# 2. 启动 JupyterHub 容器
# ==========================================

echo "正在启动 JupyterHub..."

# 尝试启动已存在的容器，如果不存在则创建并运行新容器
docker start jupyterhub || docker run -d \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /export/jupyterhub/config/page_templates:/srv/jupyterhub/page_templates \
  --net jupyterhub \
  --name jupyterhub \
  --restart always \
  -p 8081:8000 \
  shu_jupyterhub
  
echo "启动成功！"