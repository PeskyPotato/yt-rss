FROM python:3.11-slim-bookworm AS builder
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --target=/deps -r requirements.txt gunicorn
COPY app.py /app/
COPY static/ /app/static/
COPY templates/ /app/templates/

FROM gcr.io/distroless/python3-debian12:nonroot
COPY --from=builder /deps /deps
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH=/deps
EXPOSE 5000
CMD ["/deps/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
