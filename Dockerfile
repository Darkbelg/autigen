FROM python:3.11-slim

WORKDIR /myapp

RUN pip install --no-cache-dir pyautogen openai
RUN pip install -qqq matplotlib numpy
RUN pip install pyyaml
RUN pip install openapi-spec-validator
RUN pip install python-docx markdown
RUN pip install mammoth
RUN pip install openapi-schema-validator