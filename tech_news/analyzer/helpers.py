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
