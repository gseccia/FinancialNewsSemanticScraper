import string
"""
Utils methods
"""


def get_dbpedia_uri(concept: str) -> str:
    # Eliminare i caratteri inutili e aggiungere il tratto basso
    # Capitalize se il testo è minuscolo
    return "http://dbpedia.org/page/" + string.capwords(concept).replace(" ", "_")


def get_ontology_uri(concept: str) -> str:
    # Eliminare i caratteri inutili e aggiungere il tratto basso
    # Capitalize se il testo è minuscolo
    return "http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#" + \
           string.capwords(concept).replace(" ", "_")