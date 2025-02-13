# https://docs.docker.com/engine/reference/builder/

FROM ghcr.io/astral-sh/uv:python3.12-bookworm

ENV DAILY_API_KEY=NOT_SET
ENV GOOGLE_API_KEY=NOT_SET
ENV GOOGLE_PROJECT_ID=NOT_SET
ENV GOOGLE_SEARCH_ENGINE=NOT_SET
ENV KATE_BOT_NAME=OTLBot
ENV KATE_SERVER_HOST=0.0.0.0
ENV KATE_SERVER_PORT=8080
ENV KATE_SERVER_URL=NOT_SET
ENV LOGURU_LEVEL=INFO

EXPOSE 8080
WORKDIR /app

RUN apt-get update && apt-get upgrade -y

COPY dist/*.whl .
RUN uv pip install --system *.whl

CMD ["kate"]
