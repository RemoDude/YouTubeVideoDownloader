from flask import Flask, render_template, request
import os
import pytube
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])


def index():
    if request.method == 'POST':
        video_url = request.form['video_url']
        download_video(video_url)
    return render_template('index.html')
   
def download_video(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    yt = pytube.YouTube(url, headers=headers)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last()


  # Sanitize the title by removing special characters
    sanitized_title = re.sub(r'[^\w\s-]', '', yt.title)
    sanitized_title = sanitized_title.strip().replace(' ', '_')

    download_folder = os.path.join(os.getcwd(), 'downloads')
    file_path = os.path.join(download_folder, sanitized_title + '.mp4')
    # stream.download(output_path='downloads', filename=sanitized_title + '.mp4')
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # file_path = os.path.join('downloads', yt.title + '.mp4')
    stream.download(output_path='downloads', filename=file_path)

if __name__ == '__main__':
    app.run(debug=True)


# Corrected URL format
# url = 'https://www.youtube.com/shorts/l8X3Ez0_F_E'

# # Create a YouTube object
# yt = pytube.YouTube(url)

# # Filter streams, order by resolution, and download the last (highest resolution) stream
# yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').last().download()
