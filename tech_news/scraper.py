import re
import cfscrape
from typing import Union, List
from parsel import Selector
import time

from database import create_news


def fetch(url: str) -> Union[None, str]:
    """
    Returns a text with all the HTML of the page

    Parameters:
        url (str): URL of a website

    Returns:
        fetch (str): Page HTML converted to text or None
    """

    try:
        requests = cfscrape.create_scraper()
        response = requests.get(url)
        time.sleep(3)

        if response.status_code != 200:
            return None

        return response.text
    except requests.ReadTimeout:
        return None


def scrape_novidades(html_content: str) -> List[str]:
    """
    Returns a list of links

    Parameters:
        html_content (str): A text with HTML

    Returns:
        scrape_novidades (str): Returns a list of links or empty list
    """
    selector = Selector(text=html_content)
    list_news_links = selector.css("div header h2 a::attr(href)").getall()

    return list_news_links


def scrape_next_page_link(html_content: str) -> Union[str, None]:
    """
    Returns a list of links

    Parameters:
        html_content (str): A text with HTML

    Returns:
        scrape_next_page_link (str): Returns a links or None
    """
    selector = Selector(text=html_content)
    return selector.css(".next.page-numbers::attr(href)").get()


def scrape_noticia(html_content: str) -> dict:
    """
    Returns a list of links

    Parameters:
        html_content (str): A text with HTML

    Returns:
       scrape_noticia (str): Returns a Dict
    """

    selector = Selector(text=html_content)

    dict_news = {
        "url": selector.css("link[rel=canonical]::attr(href)").get(),
        "title": selector.css("h1.entry-title::text").get(),
        "timestamp": selector.css("li.meta-date::text").get(),
        "writer": selector.css(".url.fn.n::text").get(),
        "comments_count": 0,
        # https://www.codegrepper.com/code-examples/html/regex+to+remove+html+tags+python
        "summary": re.compile("<.*?>")
        .sub("", selector.css("div p").getall()[0])
        .replace("amp;", ""),
        "tags": selector.css("a[rel=tag]::text").getall(),
        "category": selector.css(
            ".meta-category span[class=label]::text"
        ).get(),
    }
    return dict_news


def get_tech_news(amount: int) -> List[dict]:
    """
    Save to database and return a list of dict
    Parameters:
        amount (int): Amount of articles

    Returns:
       get_tech_news (int): Returns a dict list
    """

    url = "https://blog.betrybe.com"  # url has no slash at the end.
    news_list = []
    news_dict_list = []

    # this loop fetches all links and saves to the list
    while True:
        html_content = fetch(url)
        news_list.extend(scrape_novidades(html_content))
        if len(news_list) >= amount:
            news_list = news_list[:amount]
            break
        url = scrape_next_page_link(html_content)

    for article in news_list:
        html_content = fetch(article)
        news_dict_list.append(scrape_noticia(html_content))
    create_news(news_dict_list)
    return news_dict_list

