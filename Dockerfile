# Use official slim Python 3.10
FROM python:3.10-slim-bullseye

# 1) Set working directory
WORKDIR /app

# 2) Copy & install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) Copy all your code, models, data
COPY . .

# 4) Run main.py by default
ENTRYPOINT ["python", "main.py"]

# 5) Default args: input folder and output folder
CMD ["pdfs_input/sample1", "output"]
