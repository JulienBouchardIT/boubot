#
#
#
FROM python:3.7

COPY requirements.txt /tmp/

RUN pip install --requirement /tmp/requirements.txt

COPY src/boubot.py /app/

WORKDIR /app

EXPOSE 80

CMD python boubot.py