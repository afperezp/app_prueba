FROM python:3.6
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["manage.py"]