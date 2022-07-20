import re
from tech_news.database import search_news


# Requisito 6
def search_by_title(title: str) -> list:
    """Faz uma busca no banco de dados de notícias por 'title'
    e retorna uma lista de tuplas contendo o 'título' e 'url' da(s) notícia(s)

    Parâmetros:
    -----------
    title : str

    Retorno:
    --------
    news_list : list[tuple]
        Uma lista com as tuplas de notícias encontradas
    """
    regex_expr = re.compile(title, flags=re.IGNORECASE)
    news_list = search_news({"title": {"$regex": regex_expr}})
    if len(news_list):
        news_list = [(news["title"], news["url"]) for news in news_list]
    return news_list


# Requisito 7
def search_by_date(date):
    """Seu código deve vir aqui"""


# Requisito 8
def search_by_tag(tag):
    """Seu código deve vir aqui"""


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
