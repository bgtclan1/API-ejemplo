FROM python:3.13.5

WORKDIR /test

COPY . /test

RUN pip install -r requirements.txt

CMD ["uvicorn", "test:app", "--host", "0.0.0.0", "--port", "8000"]
