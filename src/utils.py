import string
"""
Utils methods
"""


def get_dbpedia_uri(concept: str) -> str:
    # Eliminare i caratteri inutili e aggiungere il tratto basso
    # Capitalize se il testo è minuscolo
    return "http://dbpedia.org/page/" + string.capwords(concept).replace(" ", "_")