from ast import Return
import requests
import json
import re 
from bs4 import BeautifulSoup
from datetime import timedelta, date

websites = [
    { 
        "url" : "https://georgiatoday.ge/category/politics/",
        "scraper": "one"
    }
]


def get_news(website):
    html = get_soup(website["url"])
    if website["scraper"] == "one":
        body = scraper_one(html, website)
    return body


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def scraper_one(html, website):
    article_no = 0
    print(f'Scraping article {article_no + 1} from {website["url"]}')

    article = html.find_all("article")[article_no]
    yesterdays_date = date.today() - timedelta(1)
    if article.find_all(string=yesterdays_date.strftime(f" %B %d, %Y")):
        url = article.find("a")['href']
        html = get_soup(url)
        article_no = article_no + 1
        return html.find(attrs={"class": "entry-content no-share"}).text
    else:    
        return 




    



def get_ai_prompt():
    return

def get_ai_response():
    return

def get_user_headline():
    return

def get_article_photo():
    return

def create_post():
    return

def send_post():
    return

def publish_post():
    return

if __name__=="__main__":
    print("Building")

    for website in websites:
        while True:
            article_body = get_news(website)
            if not article_body:
                break
            prompt = get_ai_prompt()
            ai_response = get_ai_response()
            headline = get_user_headline()
            photo = get_article_photo()

            post = create_post(ai_response, headline, photo)
            send_post()
            publish_post()