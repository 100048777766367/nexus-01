FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY cells/ ./cells/
COPY adapters/ ./adapters/
COPY mechanisms/ ./mechanisms/
COPY synapses/ ./synapses/
COPY engine.py .

CMD ["python", "engine.py"]
