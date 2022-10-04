import requests
from time import sleep
import parsel
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        sleep(1)
        response = requests.get(
            url, timeout=3, headers={"user-agent": "Fake user-agent"})
        response.raise_for_status()
    except (requests.HTTPError, requests.ReadTimeout):
        return
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content):
    selector = parsel.Selector(text=html_content)
    links = selector.css(".cs-overlay-link ::attr(href)").getall()
    return links


# Requisito 3
def scrape_next_page_link(html_content):
    selector = parsel.Selector(html_content)
    next_page = selector.css(".next::attr(href)").get()
    if next_page:
        return next_page
    else:
        return None


# Requisito 4
def scrape_noticia(html_content):
    selector = parsel.Selector(html_content)
    url = selector.css('head link[rel=canonical]::attr(href)').get()
    title = selector.css("h1.entry-title::text").get().strip()
    timestamp = selector.css("li.meta-date::text").get()
    writer = selector.css(".author a::text").get()

    comments_count = selector.css(".post-comments::text").get()
    if comments_count is None:
        comments_count = 0

    summary = selector.css(
        "div.entry-content > p:nth-of-type(1) *::text").getall()

    tags = selector.css("a[rel=tag]::text").getall()
    category = selector.css(".label::text").get()

    news = {
            "url": url,
            "title": title,
            "timestamp": timestamp,
            "writer": writer,
            "comments_count": comments_count,
            "summary": ''.join(summary).strip(),
            "tags": tags,
            "category": category,
            }
    return news


# Requisito 5
def get_tech_news(amount):
    url = "https://blog.betrybe.com"
    last_news = []
    while len(last_news) <= amount:
        home = fetch(url)
        for article in scrape_novidades(home):
            html = fetch(article)
            new_dict = scrape_noticia(html)
            last_news.append(new_dict)
        url = scrape_next_page_link(home)
    last_news = last_news[:amount]
    create_news(last_news)
    return last_news
