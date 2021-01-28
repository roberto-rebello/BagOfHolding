FROM python:3-alpine


WORKDIR /app/bag

# TODO only copy nedded files
ADD . .

RUN pip install -r /app/bag/requirements.txt

# Install server dependencies

# DB migration
RUN python migrate.py


# Serve application
EXPOSE 5000
CMD ["gunicorn", "/app/bag/bag_of_holding:app"]
