#
#
#
FROM python:3.7

RUN ls

WORKDIR /app

RUN ls

RUN pip install -r requirements.txt

EXPOSE 80

CMD python boubot.py