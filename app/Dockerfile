FROM continuumio/miniconda3

COPY . /app/
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD python /app/app.py
