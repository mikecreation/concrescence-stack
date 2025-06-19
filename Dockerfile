# ---- Dockerfile ----
FROM python:3.10-slim           # 1. pick a tiny base
WORKDIR /app                    # 2. set working folder
COPY . /app                     # 3. copy repo files into image
RUN pip install -r requirements.txt || true
# if you don't have requirements.txt yet, keep the line; it will simply skip
CMD ["python", "-c", "print('NEA Docker ready')"]
