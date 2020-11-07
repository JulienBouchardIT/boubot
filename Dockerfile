FROM python:3.7 AS build-env
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY src/boubot.py /app/
WORKDIR /app
EXPOSE 80

FROM gcr.io/distroless/python3
COPY --from=build-env /app /app
WORKDIR /app
CMD ["boubot.py", "/app"]
