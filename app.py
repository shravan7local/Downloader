from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
from io import BytesIO
import tempfile
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Create temporary file (auto-deleted after closed)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp4") as tmp_file:
            ydl_opts = {
                'outtmpl': tmp_file.name,
                'format': 'best',
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Read video into memory
            tmp_file.seek(0)
            video_stream = BytesIO(tmp_file.read())

        # Send in-memory video
        return send_file(
            video_stream,
            mimetype='video/mp4',
            as_attachment=True,
            download_name='video.mp4'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/privacy.html')
def privacy():
    return render_template('privacy.html')

@app.route('/terms.html')
def terms():
    return render_template('terms.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)
