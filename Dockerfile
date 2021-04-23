FROM python:3.6

ENV PYTHONUNBUFFERED=1
ENV FLASK_APP run.py

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "coinmena.wsgi"]
