FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app.py ./

EXPOSE 5000
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:5000", "app:app"]
