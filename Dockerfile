FROM python:3
WORKDIR /usr/src/SimpleWebServer
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "main.py" ]