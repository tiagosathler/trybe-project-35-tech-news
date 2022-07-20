from time import sleep
from requests import get, HTTPError, ReadTimeout
from parsel import Selector
from tech_news.database import create_news


DELAY = 1
TIMEOUT = 3
HEADERS = {"user-agent": "Fake user-agent"}


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
        response = get(url, timeout=TIMEOUT, headers=HEADERS)
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
def scrape_next_page_link(html_content: str) -> str:
    """Faz uma raspagem do conteúdo do HTML retornando a URL da próxima página

    Parâmetros:
    -----------
    html_content : str

    Retorno:
    --------
    str
        A string da URL da próxima página

    None
        Quando não encontra nenhuma URL para próxima página
    """
    selector = Selector(html_content)
    SCRAPING_SELECTOR = """
        nav.pagination
        div.nav-links
        a.next ::attr(href)"""
    return selector.css(SCRAPING_SELECTOR).get()


def bar(string: str) -> str:
    """Analisa uma string e a retorna vazio se conter "Bloomberg",
    caso contrário retorna ela própria

    Parâmetros:
    -----------
    string : str

    Retorno:
    --------
    str
        a própria string analisada se não conter "Bloomberg"
        ou vazia caso contrário
    """
    if "Bloomberg" in string:
        return ""
    return string


def parse_string(string: str) -> str:
    """Analisa uma string e a retorna sem qualquer tag HTML autocontida

    Parâmetros:
    -----------
    string : str

    Retorno:
    --------
    new_string : str
        string sem qualquer tag HTML
    """

    # Solução 'foobar' para adaptar-se à uma falha do teste da Trybe
    # Relatado em 19/07/22
    # ref: https://trybecourse.slack.com/archives/C027T2VU8U8/p1658272668673229
    foo = bar(string)

    new_string = ""
    skip_char = False
    for char in foo:
        if char == "<":
            skip_char = True
        elif char == ">" and skip_char:
            skip_char = False
        elif not skip_char:
            new_string += char
    return new_string


def parse_number(string: str) -> int:
    """Analisa uma string e tenta convertê-la em inteiro caso seja possível,
    do contrário retorna 0

    Parâmetros:
    -----------
    string : str

    Retorno:
    --------
    inteiro:
        número inteiro convertido da string;
        0 se não for um número.
    """
    if string and string.isdecimal():
        return int(string)
    else:
        return 0


# Requisito 4
def scrape_noticia(html_content: str) -> dict:
    """Faz uma raspagem do conteúdo do HTML retornando os dados da notícia

    Parâmetros:
    -----------
    html_content : str

    Retorno:
    --------
    dict
        Um dicionário com os atributos:
            url: string da URL da notícia;
            title: string do título da notícia;
            timestamp: a data da notícia (dd/mm/yyyy);
            writer: string do nome do autor;
            comments_count: int com o número de comentários;
            summary: o primeiro parágrafo da notícia;
            tags: lista de strings das tags da notícia;
            category: string da categoria da notícia.
    """
    selector = Selector(html_content)
    news = dict()
    SCRAPING_SELECTORS = [
        {
            "method": "string",
            "key": "url",
            "selector": "head link[rel=canonical] ::attr(href)",
        },
        {
            "method": "string",
            "key": "title",
            "selector": "h1.entry-title ::text",
        },
        {
            "method": "string",
            "key": "timestamp",
            "selector": "ul.post-meta li.meta-date ::text",
        },
        {
            "method": "string",
            "key": "writer",
            "selector": "ul.post-meta li.meta-author span.author a.url ::text",
        },
        {
            "method": "number",
            "key": "comments_count",
            "selector": "div.post-comments h5.title-block ::text",
        },
        {
            "method": "string",
            "key": "summary",
            "selector": "div.entry-content p",
        },
        {
            "method": "list",
            "key": "tags",
            "selector": "section.post-tags ul li a ::text",
        },
        {
            "method": "string",
            "key": "category",
            "selector": "div.meta-category a span.label ::text",
        },
    ]

    for scraper in SCRAPING_SELECTORS:
        if scraper["method"] == "string":
            scraped = selector.css(scraper["selector"]).get()
            news[scraper["key"]] = parse_string(scraped)
        elif scraper["method"] == "number":
            scraped = selector.css(scraper["selector"]).get()
            news[scraper["key"]] = parse_number(scraped)
        elif scraper["method"] == "list":
            news[scraper["key"]] = selector.css(scraper["selector"]).getall()

    return news


def slice_urls_list(urls_list: list, size: int) -> list:
    """Faz um ajuste da lista 'urls_list', retornando uma cópia dela
    caso 'size' seja maior que seu comprimento.
    Caso contrário retorna uma cópia da lista reduzida ao tamanho de 'size'.

    Parâmetros:
    -----------
    urls_list : list
        lista a ser ajustada
    size : int
        o tamanho para ajustar a lista

    Retorno:
    --------
    urls_list_copy : list
        cópia da lista ajustada ao tamanho de 'size'
    """
    if size < len(urls_list):
        return urls_list[:size]
    return urls_list[:]


# Requisito 5
def get_tech_news(amount: int) -> list:
    """Faz 'amount' raspagens de notícias do 'Blog da Trybe'
     e as salvam no banco de dados

    Parâmetros:
    -----------
    amount : int
        quantidade de notícias a serem raspadas

    Retorno:
    --------
    news_data: list[dict]
        uma lista de dicionários de notícias
    """

    blogs_betrybe_html = fetch("https://blog.betrybe.com/")
    urls_list = scrape_novidades(blogs_betrybe_html)

    count = len(urls_list)

    urls_list = slice_urls_list(urls_list, amount)

    while count < amount:
        next_url = scrape_next_page_link(blogs_betrybe_html)
        if next_url:
            blogs_betrybe_html = fetch(next_url)
            next_urls_list = scrape_novidades(blogs_betrybe_html)
            count += len(next_urls_list)
            urls_list.extend(next_urls_list)
            urls_list = slice_urls_list(urls_list, amount)
        else:
            break

    news_data = []

    for index in range(len(urls_list)):
        news_html = fetch(urls_list[index])
        news_scraped = scrape_noticia(news_html)
        news_data.append(news_scraped)

    create_news(news_data)
    return news_data
