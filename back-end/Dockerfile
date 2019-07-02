FROM python:3.6
COPY ./requirements.txt /project/
WORKDIR /project
RUN pip install -r requirements.txt
COPY ./src /project/src
COPY ./data /project/data
ENTRYPOINT ["python"]
CMD ["src/server.py"]