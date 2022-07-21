import re
from tech_news.database import search_news
from datetime import datetime


def tuple_list_converter(list_dict: list) -> list:
    """Faz a conversão de uma lista de dicionários de notícias
    em uma lista de tuplas. Retorna uma lista vazia se 'list_dict'
    estiver vazia.

    Parâmetros:
    -----------
    list_dict: list[dict]
        Lista de dicionários de notícias

    Retorno:
    --------
    news_list : list[tuple] | []
        Uma lista com as tuplas de notícias ("title", "url")
        Ou uma lista vazia
    """
    news_list = [(news["title"], news["url"]) for news in list_dict]
    return news_list


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
    news_list = tuple_list_converter(news_list)
    return news_list


# Requisito 7
def search_by_date(date: str) -> list:
    """Faz uma busca no banco de dados de notícias por 'date'
    e retorna uma lista de tuplas contendo o 'título' e 'url' da(s) notícia(s)

    Parâmetros:
    -----------
    date : str
        Formato 'YYYY-MM-DD'

    Retorno:
    --------
    news_list : list[tuple]
        Uma lista com as tuplas de notícias encontradas
    """
    try:
        datetime_obj = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Data inválida")
    else:
        formatted_date = datetime_obj.strftime("%d/%m/%Y")
        news_list = search_news({"timestamp": formatted_date})
        news_list = tuple_list_converter(news_list)
        return news_list


# Requisito 8
def search_by_tag(tag: str) -> list:
    """Faz uma busca no banco de dados de notícias por 'tag'
    e retorna uma lista de tuplas contendo o 'título' e 'url' da(s) notícia(s)

    Parâmetros:
    -----------
    tag : str
        String com o nome da TAG

    Retorno:
    --------
    news_list : list[tuple]
        Uma lista com as tuplas de notícias encontradas
    """
    regex_expr = re.compile(tag, flags=re.IGNORECASE)
    news_list = search_news({"tags": {"$elemMatch": {"$regex": regex_expr}}})
    news_list = tuple_list_converter(news_list)
    return news_list


# Requisito 9
def search_by_category(category):
    """Seu código deve vir aqui"""
