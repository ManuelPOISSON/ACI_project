FROM python:3.9

RUN apt-get update
RUN apt-get install portaudio19-dev -y

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python3", "./first_test_mic.py" ]
