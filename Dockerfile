#
#
#
FROM python:3.7

RUN pip install -r requirements.txt

WORKDIR /app

EXPOSE 80

CMD python boubot.py