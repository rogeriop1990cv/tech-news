from datetime import datetime
from typing import List
from tech_news.database import search_news


# Requisito 6
def search_by_title(title: str) -> List[tuple]:
    """
    Returns a list of tuples

    Parameters:
        title (str): Article title
    Returns:
        fetch (str): Page HTML converted to text or None
    """
    data = search_news({"title": {"$regex": title, "$options": "i"}})
    list_filter = []

    for article in data:
        new = article["title"], article["url"]
        list_filter.append(new)
    return list_filter


# Requisito 7
def validate_date(date):
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValueError("Data inválida")


def normalized_date(date):
    month_to_int = {
        "01": "janeiro",
        "02": "fevereiro",
        "03": "março",
        "04": "abril",
        "05": "maio",
        "06": "junho",
        "07": "julho",
        "08": "agosto",
        "09": "setembro",
        "10": "outubro",
        "11": "novembro",
        "12": "dezembro",
    }

    year, month, day = date.split("-")

    return f"{int(day)} de {month_to_int[month]} de {year}"


def search_by_date(date):
    validate_date(date)
    format_date = normalized_date(date)
    data = search_news({"timestamp": {"$regex": format_date, "$options": "i"}})

    list_filter = []

    for article in data:
        new = article["title"], article["url"]
        list_filter.append(new)

    return list_filter


# Requisito 8
def search_by_tag(tag):
    data = search_news({"tags": {"$regex": tag, "$options": "i"}})
    list_filter = []

    for article in data:
        new = article["title"], article["url"]
        list_filter.append(new)
    return list_filter


# Requisito 9
def search_by_category(category):
    data = search_news({"category": {"$regex": category, "$options": "i"}})
    list_filter = []

    for article in data:
        new = article["title"], article["url"]
        list_filter.append(new)
    return list_filter
