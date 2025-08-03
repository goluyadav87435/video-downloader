from flask import Flask, render_template, request, Response, send_from_directory
import subprocess
import uuid
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "No URL provided", 400

    filename = f"video_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)
    cmd = [
        'yt-dlp',
        '-f', 'bv*+ba/best',
        '-o', output_path,
        '--no-warnings',
        '--quiet',
        '--progress-template', '%(progress._percent_str)s'
    ]

    process = subprocess.Popen(cmd + [url], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)

    def generate():
        for line in process.stdout:
            if '%' in line:
                percent = line.strip().replace('\r', '').replace('\n', '')
                yield f"data:{percent}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/downloads/<path:filename>')
def serve_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
