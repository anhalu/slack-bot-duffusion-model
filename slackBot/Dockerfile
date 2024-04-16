ARG PYTHON_VERSION=3.10.0
FROM python:${PYTHON_VERSION} as base

COPY . .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Run the application.
CMD ["python", "slackBot/main.py"]