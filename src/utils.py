import string
import re
"""
Utils methods
"""


def get_dbpedia_uri(concept: str) -> str:
    # Eliminare i caratteri inutili e aggiungere il tratto basso
    # Capitalize se il testo è minuscolo
    return "http://dbpedia.org/page/" + concept


def get_ontology_uri(concept: str) -> str:
    # Eliminare i caratteri inutili e aggiungere il tratto basso
    # Capitalize se il testo è minuscolo
    return "http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#" + concept


def find_news_source(link: str) -> str:
    """From news link, returns B if Bloombergor or R if Reuters
    @:param news link as a string
    @:return B/R
    """
    return "B" if re.search('bloomberg', link, re.IGNORECASE) else "R"


def format_name(text: str) -> str:
    return re.sub('[^a-z|A-Z|&|" "]', '', text).replace(" ","_")


if __name__ == "__main__":
    text = "http://feeds.reuters.com/~r/reuters/businessNews/~3/0iLYrt1zylE/coca-cola-chooses-plastic-bottle-collection-over-aluminum-cans-to-cut-carbon-footprint-idUSKBN1XG2J6"
    print(find_news_source(text))
    print(format_name("Telefonica SA"), format_name("PepsiCo, Inc."))
