import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
from openai import OpenAI
import os
from google_images_search import GoogleImagesSearch

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_PROJECT_ID = os.environ['OPENAI_PROJECT_ID']
GCS_DEVELOPER_KEY = os.environ['GCS_DEVELOPER_KEY']
GCS_CX = os.environ['GCS_CX']
TMP_IMAGE_NAME = "article_image.tmp"

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
    yesterdays_date = date.today() - timedelta(2)
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

def get_article_photo():
    gis = GoogleImagesSearch(GCS_DEVELOPER_KEY, GCS_CX)
    params = {
        'fileType': 'jpg',
        'imgSize': 'large'
    }

    gis.search(search_params=params, path_to_dir="~/tmp", custom_image_name=TMP_IMAGE_NAME)
    return

def create_post(ai_response, headline, photo):
    return

def send_post():
    return

def publish_post():
    return

def clean_up():
    os.remove("~/tmp/" + TMP_IMAGE_NAME)
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
            prompt = get_ai_prompt(article_body, article_headline)
            ai_response = get_ai_response(prompt)
            headline = get_user_headline()
            photo = get_article_photo()

            post = create_post(ai_response, headline, photo)
            send_post()
            publish_post()
            clean_up()