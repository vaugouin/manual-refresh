FROM mirror.gcr.io/library/python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# manual-refresh.sh mounts the folder on /app; the COPY keeps the image usable alone.
COPY . /app/

CMD ["python"]
