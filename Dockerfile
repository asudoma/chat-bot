FROM python:3.12

LABEL org.opencontainers.image.authors="artem.sudoma@gmail.com"
LABEL version="1.0"
LABEL description="Chat Bot"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt-get update \
    && apt-get install -y make --no-install-recommends

COPY poetry.lock pyproject.toml ./

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction \
    && rm -rf /root/.cache/pypoetry

COPY src/ ./

CMD [ "python3", "run.py" ]
