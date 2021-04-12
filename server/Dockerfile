FROM python:3.7-slim
ARG SOURCE_DIR
ARG INTERNAL_PORT
ARG SERVICE_NAME

EXPOSE ${INTERNAL_PORT}

COPY requirements.txt .
RUN pip install -r requirements.txt

# Build arguments are not available at runtime
ENV APP_NAME=${SERVICE_NAME}
ENV PORT=${INTERNAL_PORT}

COPY ${SOURCE_DIR} .

ENTRYPOINT uvicorn ${APP_NAME}:app --host="0.0.0.0" --port ${PORT}
