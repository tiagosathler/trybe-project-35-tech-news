from time import sleep
from requests import get, HTTPError, ReadTimeout
from parsel import Selector


DELAY = 1
TIMEOUT = 3


# Requisito 1
def fetch(url: str):
    """Faz uma requisição a uma URL e retorna o conteúdo do HTML em string

    Parâmetros:
    -----------
    url : str

    Retorno:
    --------
    str
        O conteúdo HTML da URL quando encontrada

    None
        Quando não encontrada ou timeout estourado
    """
    sleep(DELAY)
    try:
        response = get(url, timeout=TIMEOUT)
        response.raise_for_status()
    except (HTTPError, ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content: str) -> list:
    """Faz uma raspagem do conteúdo do HTML retornando uma lista de URLs

    Parâmetros:
    -----------
    html_content : str

    Retorno:
    --------
    list(str)
        Uma lista de strings das URLs de notícias encontradas nos cards

    list()
        Uma lista vazia quando não encontra nenhuma URL de notícias
    """
    selector = Selector(html_content)
    urls = list()
    articles = selector.css("div.archive-main > article.entry-preview")
    SCRAPING_SELECTOR = """
        div.post-inner
        header.entry-header
        h2.entry-title
        a ::attr(href)"""

    for article in articles:
        url = article.css(SCRAPING_SELECTOR).get()
        if url:
            urls.append(url)
    return urls


# Requisito 3
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""


# Requisito 4
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
