FROM python:3.11-slim

WORKDIR /myapp

RUN pip install --no-cache-dir pyautogen openai
RUN pip install -qqq matplotlib numpy