FROM python:3.10-alpine 

WORKDIR /code
COPY requirements.txt /code
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-u","app.py"]