from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    all_news = search_news({'title': {"$regex": title, '$options': 'i'}})
    return [(news['title'], news['url']) for news in all_news]


# Requisito 7
def search_by_date(date):
    try:
        data = []
        formated_date = datetime.fromisoformat(date).strftime("%d/%m/%Y")
        news = {
            "timestamp": {"$regex": formated_date, "$options": "i"}
        }
        date_collection = search_news(news)
        for date in date_collection:
            data.append((date["title"], date["url"]))
        return data
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_tag(tag):
    news = []
    filtered_news = search_news({"tags": {"$regex": tag, "$options": "i"}})
    for new in filtered_news:
        news.append((new["title"], new["url"]))
    return news


# Requisito 9
def search_by_category(category):
    noticias = search_news({"category": {"$regex": category, "$options": "i"}})
    serialized_search = [
        (article["title"], article["url"])for article in noticias]
    return serialized_search
