from src.brmapping import *
import json


class InfoLookup():
    """
    Class constructor and initializes the lookup tables
    """
    def __init__(self):
        self.__person_table = None
        self.__market_table = None

    """
    Load a lookup table for persons in the knowledge base
    @:param person_table filename of the json file containing the table of information about persons
    @:return None
    """
    def set_person_table(self, person_table):
        with open(person_table, mode='r') as file:
            self.__person_table = json.load(file)

    """
    Load a lookup table for stock exchanges in the knowledge base
    @:param person_table filename of the json file containing the table of information about stock exchanges
    @:return None
    """
    def set_market_table(self, market_table):
        with open(market_table, mode='r') as file:
            self.__market_table = json.load(file)

    """
    Identifies uniquely the type of a company by checking a predefined lookup table 
    @:param cat indicates the company category
    @:return The exact type of the company
    """
    def company_type_lookup(self, cat: str) -> str:
        return remove_whitespaces(br_classes[cat])

    """
    Looks for a person cited in the title of a news into the lookup knowledge of the system 
    @:param title indicates the title of the news
    @:param person_name indicates the name of a specific person to lookup
    @:return The URI of the person if found, None otherwise
    """
    def person_lookup(self, title: str=None, person_name: str=None) -> str:
        # formattare le stringhe dei nomi nello stesso modo (lowercase eliminare spazi e altri caratteri)
        if person_name in self.__person_table:
            return self.__person_table[person_name]["uri"]
        else:
            return None

    """
    Looks for a market index cited in the title of a news into the lookup knowledge of the system 
    @:param index_name indicates the name of the stock market
    @:return The URI of the market index if found, None otherwise
    """
    def market_index_lookup(self, stock_name: str) -> str:
        # formattare le stringhe dei nomi nello stesso modo (lowercase eliminare spazi e altri caratteri)
        if stock_name in self.__market_table:
            return self.__market_table[stock_name]["uri"]
        else:
            return None


    """
    Looks for a nation cited in the title of a news into the lookup knowledge of the system 
    @:param nation_name indicates the name of the nation
    @:return The URI of the nation if found, None otherwise
    """
    def nation_lookup(self, nation_name: str) -> str:
        pass


    def lookup(self, title: str) -> str:
        return None, None, None
