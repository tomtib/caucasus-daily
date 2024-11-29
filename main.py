import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
from openai import OpenAI
import os
from google_images_search import GoogleImagesSearch
from PIL import Image
import string
import random
import glob

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_PROJECT_ID = os.environ['OPENAI_PROJECT_ID']
GCS_DEVELOPER_KEY = os.environ['GCS_DEVELOPER_KEY']
GCS_CX = os.environ['GCS_CX']
TMP_IMAGE_NAME = "article_image.tmp"
HTML_TEMPLATE = "post_template.html"

WEBSITES = [
    { 
        "name": "GeorgiaToday",
        "url" : "https://georgiatoday.ge/category/politics/",
        "scraper": "one"
    }
]


def get_news(website, article_no):
    html = get_soup(website["url"])
    if website["scraper"] == "one":
        article_no, body, headline = scraper_one(html, website, article_no)
    return article_no, body, headline


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def scraper_one(html, website, article_no):
    print(f'Scraping article {article_no + 1} from {website["url"]}')


    article = html.find_all("article")[article_no]
    yesterdays_date = date.today() # - timedelta(1)
    if article.find_all(string=yesterdays_date.strftime(f" %B %d, %Y")):
        url = article.find("a")['href']
        html = get_soup(url)
        body = html.find(attrs={"class": "entry-content no-share"}).text
        headline = html.find(attrs={"class": "jeg_post_title"}).text
        article_no = article_no + 1
        return article_no, body, headline
    else:    
        return article_no, None, None


def get_ai_prompt(article_body, article_headline):
    important_points_string = "Please re-write this article in under 150 words in order of the most important points, each point being a sentence with a higher density of information - "
    conclude_string = "If the article is still under 150 words, please write another few sentences that add any left out information and conclude the article. Please provide the re-write in a default format with spaces between sentences. The article says - "
    
    print("\n" + article_headline.upper() + "\n")
    print(article_body)

    important_points_input = input("Important points (bulleted list):")
    prompt = important_points_string + important_points_input + "\n" + conclude_string + article_body

    return prompt

def get_ai_response(prompt): 
    client = OpenAI(
        organization="org-C3Iqj4sth4k8uqGtaJh96wJx",
        project=OPENAI_PROJECT_ID,

    )
    response = client.chat.completions.create (
        model="gpt-4o-mini",
        messages=[
            { 
                "role": "user",
                "content" : prompt
            }
        ]
    )
    response_body = response.choices[0].message.content
    print(response_body)

    return 

def get_user_headline():

    headline = input("Type in headline: ")
    return headline

def get_article_photo(random_file_name):
    gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
    params = {
        'q': '...',
        'num': 1,
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived',
        'fileType': 'jpg',
        'imgSize': 'large'
    }

    print("Downloading image...")
    gis.search(search_params=params, path_to_dir="tmp/", custom_image_name=random_file_name)
    image = Image.open('tmp/' + random_file_name + '.jpg')
    cropped_image = crop_image(image)
    rgb_image = cropped_image.convert('RGB')
    rgb_image.save('tmp/' + random_file_name + '.jpg')

    return

def crop_image(image):
        min_size = 700
        # Get the size of the image
        width, height = image.size

    # Calculate the new dimensions for resizing (keep the aspect ratio)
        if width < height:
            new_width = min_size
            new_height = int((min_size / width) * height)
        else:
            new_height = min_size
            new_width = int((min_size / height) * width)

        # Resize the image
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)

        # Now crop the image to square, keeping it centered
        left = (new_width - min_size) / 2
        top = (new_height - min_size) / 2
        right = (new_width + min_size) / 2
        bottom = (new_height + min_size) / 2

        # Crop the image
        cropped_image = resized_image.crop((left, top, right, bottom))

        return cropped_image


def get_tag():
    print("Please choose a tag:")
    tag_map = {
        "1": "Politics",
        "2": "Economy",
        "3": "Conflict",
        "4": "Human Rights",
        "5": "Industry",
        "6": "World"
    }
    print(tag_map)
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if choice in [1, 2, 3, 4, 5, 6]:
                return tag_map[str(choice)]
            else:
                print("Invalid choice. Please select a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def create_post(ai_response, headline, tag, random_file_name):
    todays_date = date.today()
    todays_date_formatted = todays_date.strftime(f" %B %d, %Y")

    with open(HTML_TEMPLATE, 'r') as file:
        html_template = file.read()
        filled_template = html_template.replace('{{date}}', todays_date_formatted).replace('{{tag}}', tag). replace('{{headline}}', headline).replace('{{body}}', ai_response)

    finished_post = open('tmp/' + random_file_name + '.html', "x")
    finished_post.write(filled_template)
    finished_post.close()
    return

def publish_post():
    
    return

def clean_up(random_file_name):
    files = glob.glob('tmp/*')
    for f in files:
        os.remove(f)
    return

if __name__=="__main__":
    print("Starting...")

    for website in WEBSITES:
        print(f"Scraping {website['name']}...")
        article_no = 0
        while True:
            article_no, article_body, article_headline = get_news(website, article_no)
            if not article_body:
                print(f"Article {article_no + 1} not found")
                break
            
            random_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            prompt = get_ai_prompt(article_body, article_headline)
            ai_response = get_ai_response(prompt)
            headline = get_user_headline()
            get_article_photo(random_file_name)
            tag = get_tag()
            
            create_post(ai_response, headline, tag, random_file_name)
            publish_post()
            clean_up(random_file_name)