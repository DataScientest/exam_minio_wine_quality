FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir uv
RUN uv venv && \
    . .venv/bin/activate
RUN uv pip install --no-cache-dir -r requirements.txt

CMD ["/app/.venv/bin/pytest", "-v", "-s", "/app/tests.py"]