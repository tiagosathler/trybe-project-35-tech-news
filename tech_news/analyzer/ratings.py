from tech_news.database import find_news
from tech_news.analyzer.helpers import tuple_list_converter


def multi_sort(current_list: list, criteria: tuple) -> list:
    """
    Faz a multi-ordenação de uma lista de dicionários

    Parâmetros:
    -----------
    current_list: list[dict]
        Uma lista contendo os dicionários a serem classificados

    criteria: tuple(('first_key', bool), ('second_key', bool), ...)
        Uma tupla de tuplas contendo, em ordem de ordenação, o nome da 'chave'
        do dicionário e a condição bool para ordem reversa

    Retorno:
    --------
    news_list : list[dict]
        Uma lista de dicionários multi-ordenada conforme criteria

    Nota:
        Inspirado na solução da Documentação Oficial do Python:
        https://docs.python.org/pt-br/3/howto/sorting.html#sort-stability-and-complex-sorts
    """
    for key, reverse in reversed(criteria):
        current_list.sort(key=lambda news: news[key], reverse=reverse)
    return current_list


# Requisito 10
def top_5_news() -> list:
    """Faz uma busca no banco de dados de notícias, classificando-as
    pelas popularidade de comentários e em desempatando alfabeticamente
    pelo título. Retorna pelo menos as 5 notícias mais populares.

    Parâmetros:
    -----------
    None

    Retorno:
    --------
    news_list : list[tuple]
        Uma lista com pelo menos 5 tuplas das notícias mais populares
        e desempatando-as pelo título
    """
    news_list = find_news()
    criteria = (('comments_count', True), ('title', False))
    news_list = multi_sort(news_list, criteria)
    news_list = tuple_list_converter(news_list)
    if len(news_list) < 5:
        return news_list
    else:
        return news_list[0:5]


# Requisito 11
def top_5_categories():
    """Seu código deve vir aqui"""
