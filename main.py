from flask import Flask, jsonify
from flask_cors import CORS
import instaloader
import requests
import base64

app = Flask(__name__)
CORS(app)

def download_instagram_post(post_url):
    # Create an Instaloader instance
    loader = instaloader.Instaloader()

    # Load the post by its URL
    post = instaloader.Post.from_shortcode(loader.context, post_url)

    # Check if the post is a video
    if post.is_video:
        # Get video URL
        video_url = post.video_url

        # Download video using requests
        # response = requests.get(video_url)
        # video_data = response.content

        # Convert video data to base64
        # video_base64 = base64.b64encode(video_data).decode('utf-8')

        # Return video data as base64
        return {"media_type": "video", "data": video_url}
    else:
        # Download image
        # You can modify this part as needed based on your requirements
        loader.download_post(post, target=f"{post.owner_username}_{post.shortcode}")
        image_path = f"{post.owner_username}_{post.shortcode}.jpg"

        # Return image path
        return {"media_type": "image", "path": image_path}

@app.route('/download_ig/<post_url>')
def download_ig(post_url):
    # Call the download_instagram_post function
    response = download_instagram_post(post_url)
    
    return jsonify(response)
@app.route('/')
def index():
    return "HELLO FROM SERVER"

# if __name__ == '__main__':
#     app.run(debug=True)
