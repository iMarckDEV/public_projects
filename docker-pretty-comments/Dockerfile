FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pretty_comment.py .

CMD ["python", "-u", "pretty_comment.py"]