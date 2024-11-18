from flask import Flask, request, render_template
import yt_dlp

app = Flask(__name__)

@app.route("/")
def index():
    url = request.args.get('url', type = str)
    if not url:
        return render_template("index.html")

    ydl_opts = {
        'playlist_items': '0',
        'print': 'channel_url'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    channel_id = info.get("channel_id")
    data = {
        "channel_id": channel_id,
        "feed_url": f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}",
        "webpage_url": info.get("webpage_url")
    }
    return render_template("index.html", data=data)
