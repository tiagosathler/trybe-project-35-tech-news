import re
from tech_news.database import search_news
from datetime import datetime
from tech_news.analyzer.helpers import tuple_list_converter


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
def search_by_category(category: str) -> list:
    """Faz uma busca no banco de dados de notícias por 'category'
    e retorna uma lista de tuplas contendo o 'título' e 'url' da(s) notícia(s)

    Parâmetros:
    -----------
    category : str
        String com o nome da categoria

    Retorno:
    --------
    news_list : list[tuple]
        Uma lista com as tuplas de notícias encontradas
    """
    regex_expr = re.compile(category, flags=re.IGNORECASE)
    news_list = search_news({"category": {"$regex": regex_expr}})
    news_list = tuple_list_converter(news_list)
    return news_list
