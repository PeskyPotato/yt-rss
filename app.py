from flask import Flask, request, render_template, flash
import os
import yt_dlp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

@app.route("/")
def index():
    url = request.args.get('url', type = str)
    if not url:
        return render_template("index.html")

    extractors = yt_dlp.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(url) and ('youtube' not in e.IE_NAME) and (e.IE_NAME != 'generic'):
            flash(f"Unsupported URL: {url}", category="post-info")
            return render_template("index.html")

    ydl_opts = {
        'extract_flat': 'in_playlist',
        'extractor_args': {'youtube': {'player_client': ['web']}},
        'playlist_items': '0',
        'simulate': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        if "Unsupported URL" in str(e):
            flash(f"Unsupported URL: {url}", category="post-info")
        else:
            print(e, url)
            flash(f"Download Error: {url}", category="post-info")
        return render_template("index.html")

    if not info:
        flash(f"Unsupported URL: {extractor}", category="post-info")
        return render_template("index.html")

    channel_id = info.get("channel_id")
    data = {
        "channel_id": channel_id,
        "feed_url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
        "webpage_url": info.get("webpage_url")
    }

    playlist_id = info.get("id")
    if playlist_id and playlist_id.startswith("PL"):
        data["playlist_id"] = playlist_id
        data["playlist_feed_url"] = f"https://www.youtube.com/feeds/videos.xml?playlist_id={playlist_id}"

    return render_template("index.html", data=data)
