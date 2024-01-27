FROM python:3.8.16

RUN mkdir execute
WORKDIR /execute
COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

ENTRYPOINT ["python3", "main.py", "--start_day 20101001", "--end_day 20231231", "--split 12"]