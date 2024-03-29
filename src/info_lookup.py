from src.brmapping import *
from src.ner import text_ner
from src.utils import get_ontology_uri, format_name
import json
import re


class InfoLookup():
    """
    Class constructor and initializes the lookup tables
    """
    def __init__(self):
        self.__person_table = None
        self.__market_table = None
        self.__country_table = None
        self.__person_table_filename = None
        self.__market_table_filename = None
        self.__country_table_filename = None

    """
    Load a lookup table for persons in the knowledge base
    @:param person_table filename of the json file containing the table of information about persons
    @:return None
    """
    def set_person_table(self):
        with open(self.__person_table_filename, mode='r', encoding="utf-8") as file:
            self.__person_table = json.load(file)

    """
    Exposes the lookup table for persons in the knowledge base
    @:param None
    @:return persons lookup table
    """
    def get_person_table(self):
        return self.__person_table

    """
    Load a lookup table for stock exchanges in the knowledge base
    @:param person_table filename of the json file containing the table of information about stock exchanges
    @:return None
    """
    def set_market_table(self):
        with open(self.__market_table_filename, mode='r', encoding="utf-8") as file:
            self.__market_table = json.load(file)

    """
    Exposes the lookup table for stock exchange markets in the knowledge base
    @:param None
    @:return stock exchange lookup table
    """
    def get_market_table(self):
        return self.__market_table

    def set_person_table_filename(self, t: str):
        self.__person_table_filename = t

    def set_market_table_filename(self, t: str):
        self.__market_table_filename = t

    """
    Load a lookup table for countries in the knowledge base
    @:param countries_table filename of the json file containing the table of information about countries
    @:return None
    """
    def set_countries_table(self, country_table: str):
        self.__country_table_filename = country_table
        with open(country_table, mode='r', encoding="utf-8") as file:
            data = json.load(file)
            t = dict()
            for e in data:
                t[e["country"]] = e["uri"]
            self.__country_table = {k.lower(): v for k, v in t.items()}
            self.__country_table = {re.sub('[^a-z]', '', k): v for k, v in self.__country_table.items()}

    """
    Identifies uniquely the type of a company by checking a predefined lookup table 
    @:param cat indicates the company category
    @:return The exact type of the company if found, None if not
    """
    def company_type_lookup(self, cat: str):
        try:
            return remove_whitespaces(br_classes[cat])  # If found any in the keys (Reuters)
        except KeyError:
            for v in br_classes.values():
                if v == cat:
                    return remove_whitespaces(cat)  # If found any in the values (Bloomberg)
            else:
                return None  # If not found

    """
    Looks for a person cited in the title of a news into the lookup knowledge of the system 
    @:param title indicates the title of the news
    @:param person_name indicates the name of a specific person to lookup
    @:return The URI of the person if found, None otherwise
    """
    def person_lookup(self, person_name: str):
        key_to_find = person_name.lower()
        key_to_find = re.sub('[^a-z]', '', key_to_find)
        for key in self.__person_table:
            if re.sub('[^a-z]', '', key.lower()) == key_to_find:
                return self.__person_table[key]["uri"]
        else:
            return None

    """
    Looks for a market index cited in the title of a news into the lookup knowledge of the system 
    @:param index_name indicates the name of the stock market
    @:return The URI of the market index if found, None otherwise
    """
    def market_index_lookup(self, stock_name: str, default=True):
        key_to_find = stock_name.lower()
        key_to_find = re.sub('[^a-z|0-9|&]', '', key_to_find)
        key_found = None
        if default:
            for key in self.__market_table:
                if re.sub('[^a-z|0-9|&]', '', key.lower()) in key_to_find or key_to_find in re.sub('[^a-z]', '', key.lower()):
                    key_found = self.__market_table[key]
                    break
            #for key in self.__market_table.keys():
                #if key in key_to_find or key_to_find in key:
                    #key_found = self.__market_table[key]
                    #break
            return key_found
        else:
            stocks_found = list()
            for key in self.__market_table:
                if re.sub('[^a-z|0-9|&]', '', key.lower()) in key_to_find:
                    if self.__market_table[key] is not None:
                        stocks_found.append(self.__market_table[key])
            return stocks_found

    """
    Looks for a nation cited in the title of a news into the lookup knowledge of the system 
    @:param nation_name indicates the name of the nation
    @:return The URI of the nation if found, None otherwise
    """
    def country_lookup(self, country_name: str):
        key_to_find = country_name.lower()
        key_to_find = re.sub('[^a-z]', '', key_to_find)
        if key_to_find in self.__country_table.keys():
            return self.__country_table[key_to_find]
        else:
            key_found = None
            for key in self.__country_table:
                if re.sub('[^a-z|0-9|&]', '', key.lower()) in key_to_find or key_to_find in re.sub('[^a-z]', '', key.lower()):
                    key_found = self.__country_table[key]
                    break
            return key_found

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
                val = self.person_lookup(el["name"])
                if val is None:
                    # If the person found by the ner is not in the knowledge base update table and return uri
                    self.update_table(True, format_name(el["name"]), True)
                    persons.append(self.person_lookup(el["name"]))
                else:
                    # If the person is already in the knowledge base
                    persons.append(val)
            elif el['category'] == 'place':
                val = self.country_lookup(el['name'])
                if val:
                    places.append(val)
        markets = self.market_index_lookup(title, default=False)
        return persons, markets, places

    """
    Updates the knowledge base of the system
    @:param update_type if true updates persons table, otherwise updates markets table
    @:param new_individual is the unknown concept found by the system 
    @:param title_or_scrape in case of unknown persons found indicates whether this info comes from a news title (True)
            or from web scraping (False)
    @:return None
    """
    def update_table(self, update_type: bool, new_individual: str, title_or_scrape: bool=False):
        link = get_ontology_uri(new_individual)
        if update_type:
            # update persons table, the system found an unknown person
            if not title_or_scrape:
                # the person found must be a CEO of a company
                self.__person_table[new_individual] = {"uri": link, "isCeo/Chairman": True,
                                                       "hasNationalRole": False}
            else:
                self.__person_table[new_individual] = {"uri": link, "isCeo/Chairman": False,
                                                       "hasNationalRole": False}
            with open(self.__person_table_filename, 'w', encoding='utf-8') as file:
                json.dump(self.__person_table, file)
        else:
            # update stocks table, the system found an unknown stock
            self.__market_table[new_individual] = link
            with open(self.__market_table_filename, 'w', encoding='utf-8') as file:
                json.dump(self.__market_table, file)


if __name__ == "__main__":
    i = InfoLookup()
    i.set_person_table('../resources/Data/vips_original.json')
    i.set_market_table('../resources/Data/stock_exchange_original.json')
    i.set_countries_table('../resources/Data/countries.json')
    #i.update_table(False, "Ilaria Stock")
    #print(i.lookup("SoftBank Takes Control of WeWork as Part of Bailout, Adam Neumann Leaves Board in Spain, "
                   #"Italy, America. NASDAQ, CSI 300 and S&P 500 falling quickly"))
    #print(i.country_lookup("Italy"))
    #print(i.country_lookup("Ogliara"))
    print(i.person_lookup('Amancio_Ortega'))
    print(i.person_lookup('Antonio_Vicinanza'))
    print(i.update_table(False,"Nasdaq"))
    print(i.market_index_lookup("PeppeSeccia_200"))
    print(i.update_table(True, "Marco_Carpentiero"))
