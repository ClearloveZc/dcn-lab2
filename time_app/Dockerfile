FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && groupadd --gid 799 nyu \
    && useradd --uid 999 --gid nyu --no-create-home nyu
COPY --chown=nyu:nyu run.py .
USER nyu
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-class", "gthread", "--threads", "2", "--access-logfile", "-", "run:app"]
