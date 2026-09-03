FROM python:3.8
COPY ./summarize-microservice/webapp/requirements.txt ./webapp/requirements.txt 
WORKDIR /webapp
COPY summarize-microservice/webapp/* /webapp

RUN pip install -r requirements.txt
#ENTRYPOINT ["uvicorn"]
CMD ["python3","app.py"]