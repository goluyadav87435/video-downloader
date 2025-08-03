from flask import Flask, request, send_file, render_template_string
import yt_dlp
import uuid
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Video Downloader</title>
  <style>
    body { background-color: black; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; }
    input, button { padding: 10px; margin-top: 10px; font-size: 16px; width: 300px; }
    input { background-color: white; color: black; border: none; border-radius: 5px; }
    button { background-color: white; color: black; border: none; border-radius: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <h2>Paste any video link below:</h2>
  <form method="POST">
    <input type="text" name="url" placeholder="Enter video URL" required />
    <button type="submit">Download</button>
  </form>
  {% if status %}
    <p>{{ status }}</p>
  {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template_string(HTML, status="Please enter a URL.")
        
        unique_id = str(uuid.uuid4())
        output_path = f"{unique_id}.mp4"
        
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': output_path,
            'merge_output_format': 'mp4',
            'quiet': True,
            'noplaylist': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            return send_file(output_path, as_attachment=True)

        except Exception as e:
            return render_template_string(HTML, status=f"Error: {str(e)}")
        
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    return render_template_string(HTML, status=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
