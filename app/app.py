from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Path to the posts directory
    posts_dir = "static/posts/"
    # Get all files sorted by modification time
    files = sorted(os.listdir(posts_dir), key=lambda x: os.path.getmtime(os.path.join(posts_dir, x)), reverse=True)
    latest_files = files[:3]  # Get the latest three files
    return render_template("index.html", latest_files=latest_files)

# In the HTML template:
# <a href="{{ url_for('static', filename='posts/' + latest_files[0]) }}">{{ latest_files[0] }}</a>

if __name__ == '__main__':
    app.run(debug=True)
