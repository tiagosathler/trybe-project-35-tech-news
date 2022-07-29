import sys
from tech_news.scraper import get_tech_news
from tech_news.analyzer.search_engine import (
    search_by_title,
    search_by_date,
    search_by_tag,
    search_by_category,
)
from tech_news.analyzer.ratings import top_5_news, top_5_categories


def get_tech_news_menu():
    amount = input("Digite quantas notícias serão buscadas:")
    return get_tech_news(int(amount, base=10))


def search_by_title_menu():
    title = input("Digite o título:")
    return search_by_title(title)


def search_by_date_menu():
    date = input("Digite a data no formato aaaa-mm-dd:")
    return search_by_date(date)


def search_by_tag_menu():
    tag = input("Digite a tag:")
    return search_by_tag(tag)


def search_by_category_menu():
    category = input("Digite a categoria:")
    return search_by_category(category)


# Requisito 12
def analyzer_menu():
    """
    Menu interativo do analyzer.
    Retorna o resultado conforme escolha do menu.
    """
    menu_content = (
        "Selecione uma das opções a seguir:\n"
        + " 0 - Popular o banco com notícias;\n"
        + " 1 - Buscar notícias por título;\n"
        + " 2 - Buscar notícias por data;\n"
        + " 3 - Buscar notícias por tag;\n"
        + " 4 - Buscar notícias por categoria;\n"
        + " 5 - Listar top 5 notícias;\n"
        + " 6 - Listar top 5 categorias;\n"
        + " 7 - Sair."
    )

    choice = input(menu_content)

    if not (choice and choice in ["0", "1", "2", "3", "4", "5", "6", "7"]):
        print("Opção inválida", file=sys.stderr)
    elif choice == "7":
        print("Encerrando script")
    else:
        menu_dict = {
            "0": get_tech_news_menu,
            "1": search_by_title_menu,
            "2": search_by_date_menu,
            "3": search_by_tag_menu,
            "4": search_by_category_menu,
            "5": top_5_news,
            "6": top_5_categories,
        }
        return menu_dict[choice]()

    return None
