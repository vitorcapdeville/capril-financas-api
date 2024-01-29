FROM python:3.10

WORKDIR /docker_app

COPY ./requirements.txt /docker_app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /docker_app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]