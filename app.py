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
        'playlist_items': '0',
        'print': 'channel_url'
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
    
    channel_id = info.get("channel_id")
    data = {
        "channel_id": channel_id,
        "feed_url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
        "webpage_url": info.get("webpage_url")
    }
    return render_template("index.html", data=data)
