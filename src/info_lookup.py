from brmapping import *
from ner import text_ner
from utils import get_dbpedia_uri
import json
import re


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
        with open(person_table, mode='r', encoding="utf-8") as file:
            t = json.load(file)
            self.__person_table = {k.lower(): v for k, v in t.items()}
            self.__person_table = {re.sub('[^a-z]', '', k): v for k, v in self.__person_table.items()}

    """
    Load a lookup table for stock exchanges in the knowledge base
    @:param person_table filename of the json file containing the table of information about stock exchanges
    @:return None
    """
    def set_market_table(self, market_table):
        with open(market_table, mode='r', encoding="utf-8") as file:
            t = json.load(file)
            self.__market_table = {k.lower(): v for k, v in t.items()}
            self.__market_table = {re.sub('[^a-z|&]', '', k): v for k, v in self.__market_table.items()}


    def set_countries_table(self, market_table):
        with open(market_table, mode='r', encoding="utf-8") as file:
            data = json.load(file)
            for e in data:
                t = {e["country"]: e["uri"]}
                print(t)
            print(t)
            self.__market_table = {k.lower(): v for k, v in t.items()}
            self.__market_table = {re.sub('[^a-z|&]', '', k): v for k, v in self.__market_table.items()}
            print(self.__market_table)


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
    def person_lookup(self, person_name: str):
        key_to_find = person_name.lower()
        key_to_find = re.sub('[^a-z]', '', key_to_find)
        if key_to_find in self.__person_table.keys():
            return self.__person_table[person_name]["uri"]
        else:
            return None

    """
    Looks for a market index cited in the title of a news into the lookup knowledge of the system 
    @:param index_name indicates the name of the stock market
    @:return The URI of the market index if found, None otherwise
    """
    def market_index_lookup(self, stock_name: str, default=True):
        key_to_find = stock_name.lower()
        key_to_find = re.sub('[^a-z|&]', '', key_to_find)
        if default:
            if key_to_find in self.__market_table.keys():
                return self.__market_table[stock_name]
            else:
                return None
        else:
            stocks_found = list()
            for key in self.__market_table:
                if key in key_to_find:
                    if self.__market_table[key] is not None:
                        stocks_found.append(self.__market_table[key])
            return stocks_found

    """
    Looks for a nation cited in the title of a news into the lookup knowledge of the system 
    @:param nation_name indicates the name of the nation
    @:return The URI of the nation if found, None otherwise
    """
    def nation_lookup(self, nation_name: str) -> str:
        pass

    """
    Looks for persons, stock exchanges and places cited in a news title
    @:param title news title in which to look for information
    @:return tuple of lists containing persons, markets, places in the news title
    """
    def lookup(self, title: str) -> (list, list, list):
        # Call ner to obtain persons and places in a list of dict
        data = text_ner(title)
        persons, markets, places = list(), list(), list()
        for el in data:
            if el['category'] == 'name':
                persons.append(get_dbpedia_uri(el['name']))
            elif el['category'] == 'place':
                places.append(get_dbpedia_uri(el['name']))
        markets = self.market_index_lookup(title, default=False)
        return persons, markets, places

    """
    Updates the knowledge base of the system
    @:param
    """
    def update_table(self, ):
        pass


if __name__ == "__main__":
    i = InfoLookup()
    i.set_person_table('../resources/Data/vips.json')
    i.set_market_table('../resources/Data/stock_exchange.json')
    i.set_countries_table('../resources/Data/countries.json')
    print(i.lookup("SoftBank Takes Control of WeWork as Part of Bailout, Adam Neumann Leaves Board"))
