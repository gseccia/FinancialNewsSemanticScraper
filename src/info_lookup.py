from src.brmapping import *

"""
Identifies uniquely the type of a company by checking a predefined lookup table 
@:param cat indicates the company category
@:return The exact type of the company
"""
def company_type_lookup(cat: str) -> str:
    return remove_whitespaces(br_classes[cat])


"""
Looks for a person cited in the title of a news into the lookup knowledge of the system 
@:param title indicates the title of the news
@:param person_name indicates the name of a specific person to lookup
@:return The URI of the person if found, None otherwise
"""
def person_lookup(title: str=None, person_name: str=None) -> str:
    return None


"""
Looks for a market index cited in the title of a news into the lookup knowledge of the system 
@:param index_name indicates the name of the stock market
@:return The URI of the market index if found, None otherwise
"""
def market_index_lookup(index_name: str) -> str:
    return None


"""
Looks for a nation cited in the title of a news into the lookup knowledge of the system 
@:param nation_name indicates the name of the nation
@:return The URI of the nation if found, None otherwise
"""
def nation_lookup(nation_name: str) -> str:
    pass


def lookup(title: str) -> str:
    return None, None, None
