'''1. Build a Flask app that scrapes data from multiple websites and displays it on your site.
You can try to scrap websites like youtube , amazon and show data on output pages and deploy it on cloud platform in python'''

from flask import Flask, render_template
from googleapiclient.discovery import build

app = Flask(__name__)


API_KEY = 'AIzaSyA8p_pjTXmcuNDHlwXRbDBtBJ3T7K9AZcE'

def get_youtube_videos():
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.search().list(q='Python Programming', part='snippet', type='video', maxResults=10)
    response = request.execute()
    videos = [{'title': item['snippet']['title'], 'video_id': item['id']['videoId']} for item in response['items']]
    return videos

@app.route('/')
def index():
    youtube_videos = get_youtube_videos()
    return render_template('index.html', youtube_videos=youtube_videos)

if __name__ == "__main__":
    app.run(debug=True)
