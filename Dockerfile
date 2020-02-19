FROM python:slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY webcron /usr/src/app

# Entrypoint
CMD [ "python", "-u", "./webcron.py" ]

