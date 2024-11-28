from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Path to the posts directory inside templates
    posts_dir = os.path.join("templates", "posts")
    # Get all files sorted by modification time
    files = sorted(os.listdir(posts_dir), key=lambda x: os.path.getmtime(os.path.join(posts_dir, x)), reverse=True)
    raw_files = [file.split('.', 1)[0] for file in files]
    return render_template("index.html", latest_files=raw_files)

@app.route('/posts/<filename>')
def get_post(filename):
    # Dynamically serve files from the templates/posts/ directory
    posts_dir = os.path.join("templates", "posts")
    return send_from_directory(posts_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
