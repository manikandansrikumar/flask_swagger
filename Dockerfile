FROM python:3.6
RUN apt-get update
RUN apt-get install -y
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD [ "app.py" ]
