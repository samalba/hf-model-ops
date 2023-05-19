FROM python:3.10-slim-buster

COPY requirements.txt test_pipelines_summarization.py /src/
WORKDIR /src
RUN pip install -r requirements.txt

CMD ["pytest"]
