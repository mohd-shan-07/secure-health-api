FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest pytest-cov
COPY . .
EXPOSE 8443
CMD ["python","server.py"]