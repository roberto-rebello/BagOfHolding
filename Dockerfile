FROM python:3-alpine

RUN apk add --virtual .build-dependencies \
            --no-cache \
            python3-dev \
            build-base \
            linux-headers \
            pcre-dev
RUN apk add --no-cache pcre

WORKDIR /app/bag

# TODO only copy nedded files
ADD . .

RUN pip install -r /app/bag/requirements.txt

# Install server dependencies
RUN apk del .build-dependencies && rm -rf /var/cache/apk/*

# DB migration
RUN python migrate.py


# Serve application
EXPOSE 5000
CMD ["uwsgi", "--ini", "/app/bag/deploy/uwsgi.ini"]
