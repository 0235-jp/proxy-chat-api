FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN apt update && apt install -y build-essential
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]