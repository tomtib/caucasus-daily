from flask import Flask, render_template, send_from_directory
import os
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    # Path to the posts directory inside templates
    posts_dir = os.path.join("templates", "posts")
    # Get all files sorted by modification time
    files = sorted(os.listdir(posts_dir), key=lambda x: os.path.getmtime(os.path.join(posts_dir, x)), reverse=True)
    
    data = []

    for filename in files:
        # Skip non-HTML files (if any)
        if not filename.endswith(".html"):
            continue

        file_path = os.path.join(posts_dir, filename)

        # Extract data from the HTML file
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # Parse the HTML and extract the required fields
        soup = BeautifulSoup(html_content, "html.parser")
        date = soup.find("div", class_="date").get_text(strip=True) if soup.find("div", class_="date") else None
        headline = soup.find("h3").get_text(strip=True) if soup.find("h3") else None
        tag = soup.find("span", class_="bgr").get_text(strip=True) if soup.find("span", class_="bgr") else None
        body = soup.find("p", class_="about-pera1").get_text(strip=True) if soup.find("p", class_="about-pera1") else None

        raw_file = filename.split('.', 1)[0]

        data.append({
            "filename": raw_file,
            "date": date,
            "body": body,
            "headline": headline,
            "tag": tag
            })
        
    return render_template("index.html", latest_files=data)

@app.route('/posts/<filename>')
def get_post(filename):
    # Dynamically serve files from the templates/posts/ directory
    posts_dir = os.path.join("templates", "posts")
    return send_from_directory(posts_dir, filename)

if __name__ == '__main__':
    app.run(debug=True)
