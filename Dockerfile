FROM docker.io/python:3.11-alpine

CMD ["python", "-m", "http.server", "8000"]

FROM docker.io/python:3.11-alpine

WORKDIR /app

COPY requirements.txt ./

# /app으로 이동 후 requirements.txt 복사
# copy 를 해야 docker.io/python:3.11-alpine 컨테이너 안에 넣을 수 있음

RUN pip install -r requirements.txt --no-cache-dir --disable-pip-version-check

# requirements.txt 실행

ARG DJANGO_SETTINGS_MODULE
ENV DJANGO_SETTINGS_MODULE ${DJANGO_SETTINGS_MODULE:-server.settings}

# RUN python server/manage.py collectstatic

COPY ./ /app

EXPOSE 8000

WORKDIR /app/server

CMD ["gunicorn", "server.asgi:application", "-c", "conf.d/gunicorn.conf.py"]