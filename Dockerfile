# # 1) Base: Python 3.10 slim on amd64 from Google’s mirror
# FROM --platform=linux/amd64 mirror.gcr.io/library/python:3.10-slim-bullseye

# # 2) Set working dir
# WORKDIR /app

# # 3) Copy & pip‑install, forcing binary wheels only
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # 4) Copy your code, models and data
# COPY . .

# # 5) CLI entrypoint
# ENTRYPOINT ["python", "main.py"]


# Use Google’s mirror for Python 3.10 slim Bullseye on amd64
# 1) Base image that already includes Torch + CUDA/CUDNN for Python 3.10
# Use the official PyTorch CPU image for Python 3.x

# Base python image
# 1) Start from official slim Python 3.10
FROM python:3.10-slim-bullseye

# 2) Give pip more time & retries for big packages
ENV PIP_DEFAULT_TIMEOUT=1200
ENV PIP_RETRIES=5

# 3) Set working dir
WORKDIR /app

# 4) Install CPU‑only PyTorch & friends (PyPI now hosts CPU wheels)
RUN pip install --no-cache-dir \
        torch==2.7.1 \
        torchvision==0.18.2 \
        torchaudio==2.7.2

# 5) Copy & install your remaining (much smaller) deps
COPY requirements-lite.txt .
RUN pip install --no-cache-dir --prefer-binary -r requirements-lite.txt

# 6) Copy the rest of your app: code, models, data folders
COPY . .

# 7) Run your CLI exactly as you do locally
ENTRYPOINT ["python", "main.py"]

# Default arguments: input folder and output folder
CMD ["pdfs_input/sample1", "output"]
