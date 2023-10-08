FROM python:3.11.6-alpine3.18

RUN pip install confar

WORKDIR /app

ENTRYPOINT [ "confar", "run", "config.yml" ] 