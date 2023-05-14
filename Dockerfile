# get python image of the current version
FROM python:3.11.3-buster

# set default directory to /app
WORKDIR /app

# copy stuff over
COPY requirements.txt requirements.txt

RUN apt-get update && apt-get upgrade -y
RUN python -m venv .venv
# source command may not be avaiable in the shell, use . 
RUN . .venv/bin/activate

RUN apt-get install libsnappy-dev -y
RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

# Make port 8050 available to the world outside this container
EXPOSE 8050

# copy file from local machine ./app to remote . (which is /app)
COPY ./app .


# run the script
CMD ["python3", "app.py"]