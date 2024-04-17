ARG PYTHON_VERSION=3.10.0
FROM python:${PYTHON_VERSION} as base

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

# Run the application.
CMD ["python", "main.py"]
