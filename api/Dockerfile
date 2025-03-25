FROM python:3.11-slim
WORKDIR /app

RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 配置 pip 国内镜像源
ENV PIP_INDEX_URL=https://pypi.mirrors.ustc.edu.cn/simple/
ENV PIP_EXTRA_INDEX_URL=https://mirrors.cloud.tencent.com/pypi/simple/

COPY requirements.txt .
RUN pip install --no-cache-dir wheel setuptools
RUN pip install --no-cache-dir paddlepaddle
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 9988
CMD ["python3", "main.py"]