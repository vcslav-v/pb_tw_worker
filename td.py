from bs4 import BeautifulSoup
import requests
import db
import models
import os

TD_URL = os.environ.get('TD_URL')

def _get_new_articles() -> str:
    resp = requests.get(TD_URL)
    soup = BeautifulSoup(resp.content, 'lxml')
    soup_articles = soup.find(
        'div', attrs = {'class': 'jeg_latestpost'}
    ).find_all(
        'article'
    )
    article_links = []
    for soup_article in soup_articles:
        article_links.append(soup_article.a['href'])
    with db.SessionLocal() as session:
        posted_articles = session.query(models.PostedTDarticle).filter(models.PostedTDarticle.url.in_(article_links)).all()
    posted_articles = set([arcicle.url for arcicle in posted_articles])
    article_links = set(article_links)
    for_posting_urls = article_links - posted_articles
    if not for_posting_urls:
        return ''
    return for_posting_urls.pop()


def _get_discription(url: str) -> str:
    article_resp = requests.get(url)
    soup = BeautifulSoup(article_resp.content, 'lxml')
    title = soup.h1.text
    sub_title = soup.h2.text
    return f'{title}\n{sub_title}'

def get_new_article_post():
    posting_url = _get_new_articles()
    if not posting_url:
        return
    discription = _get_discription(posting_url)
    return (posting_url, discription)

def add_posted_article(url: str):
    article = models.PostedTDarticle(
        url=url,
    )
    with db.SessionLocal() as session:
        session.add(article)
        session.commit()
