FROM python:3.11-slim

WORKDIR /myapp

RUN pip install --no-cache-dir pyautogen openai