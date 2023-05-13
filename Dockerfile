# get python image of the current version
FROM python:3.11.3-slim-buster

# set default directory to /app
WORKDIR /app

# copy stuff over
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# copy file from local machine ./app to remote .
COPY ./app .

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]