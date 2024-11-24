# yt-rss

A Flask app to generate a YouTube channel RSS feed from the channel URL.

## Build and Run

The Flask app is built to run in a Docker container. Follow the steps below to get started.

```bash
docker build -t ytrss:latest .
docker compose up -d
```

Remember to change the `SECRET_KEY` environment variable in the `docker-compose.yml` file. The app will be accessible on 0.0.0.0:5005.

## LICENSE

Distributed under the MIT License, see `LICENSE` for more information.
