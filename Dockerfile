FROM python:3-alpine

WORKDIR /app/bag

# Copy nedded files
COPY bag_of_holding.py .
COPY migrate.py .
COPY requirements.txt .
COPY static static
COPY templates templates

# Create db folder
RUN mkdir db/

# Install requirements
RUN pip install -r requirements.txt

# DB creation
RUN python migrate.py

# Serve application
EXPOSE 8000
CMD ["gunicorn", "-b 0.0.0.0:8000", "bag_of_holding:app"]
