from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "👋 Instagram Video Downloader is running."

@app.route("/download", methods=["POST"])
def download_video():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL missing"}), 400

    ydl_opts = {
        'skip_download': True,
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
        'simulate': True,
        'forceurl': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get("url") or info.get("entries", [{}])[0].get("url")
            return jsonify({"download_url": video_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

