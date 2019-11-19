from src.fuseki_wrapper import FusekiSparqlWrapper
from src.topic_classifier import TopicClassifier
from src.fsanalysis import *
from src.info_lookup import *
from src.utils import get_dbpedia_uri, find_news_source, format_name


class Tripleizer():
    """ Class constructor """

    def __init__(self):
        self.__db_manager = FusekiSparqlWrapper()
        classes = {0: 'CompaniesEconomy', 1: 'Markets&Goods', 2: 'NationalEconomy', 3: 'OtherTopic'}
        self.__topic_classifier = TopicClassifier(classes_dict=classes,
                         tokenizer_path='../resources/keras_model_classifier/tokenizer.pickle',
                         path_to_h5_classifier="../resources/keras_model_classifier/model.h5")
        self.__query_prefix = """
        PREFIX ont: <http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        """
        self.__insert_prefix = "INSERT DATA {"
        self.__delete_prefix = "DELETE DATA {"
        self.__analyser = FinancialSentimentAnalysis()
        self.__lookuper = InfoLookup()
        self.__lookuper.set_person_table("../resources/Data/vips.json")
        self.__lookuper.set_market_table('../resources/Data/stock_exchange.json')
        self.__lookuper.set_countries_table('../resources/Data/countries.json')
        # populate the ontology with the a priori knowledge
        self.load_persons_and_markets()

    """
    Generates an insert query for an RDF triples storage. 
    @:param news_pool FinViz scraped news data
    @:return string representing the insert query
    """
    def generate_insert(self, news_pool: dict):
        # as first operation generate an insert query using the news pool data
        partial_query = self.__query_prefix
        partial_query = partial_query + self.__insert_prefix

        for news in news_pool:  # news is the link
            datetime = news_pool[news]["date"]
            news_title = news_pool[news]["text"]
            news_source = find_news_source(news)
            partial_query = partial_query + "\n<" + news + "> rdf:type ont:News, owl:NamedIndividual ."
            partial_query = partial_query + '\n<' + news + '> ont:hasTitle "' + news_title + '"^^xsd:string .'
            partial_query = partial_query + '\n<' + news + '> ont:hasDateTime "' + datetime + '"^^xsd:dateTime .'

            # news topic is defined by the ML classifier
            print(self.__topic_classifier.classify_news(news_title))
            macro_topic, specific_topic = self.__topic_classifier.classify_news(news_title)
            if macro_topic == "EconomicsTopics":
                partial_query = partial_query + "\n<" + news + "> ont:hasEconomicsTopic ont:" + specific_topic + " ."
            else:
                partial_query = partial_query + "\n<" + news + "> ont:hasOtherTopic ont:" + specific_topic + " ."

            # add news sentiment positiveness
            partial_query = partial_query + '\n<' + news + '> ont:hasPositivenessRank "' + \
                            self.__analyser.sentiment_analysis(news_title) + '"^^xsd:float .'

            if news_source == "B":
                # news retrieved from Bloomberg
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <ont:Bloomberg_News> ."
            elif news_source == "R":
                # news retrieved from Reuters
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <ont:Reuters> ."
            else:
                # news retrieved from other publishers
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <ont:News_agency> ."

            # build citation in news title triples
            person_list, market_list, nation_list = self.__lookuper.lookup(news_title)

            if person_list:
                for person_uri in person_list:
                    partial_query = partial_query + "\n<" + person_uri + "> ont:isCitedIn <" + news + "> ."

            if market_list:
                for market_uri in market_list:
                    partial_query = partial_query + "\n<" + market_uri + "> ont:isCitedIn <" + news + "> ."

            if nation_list:
                for nation_uri in nation_list:
                    partial_query = partial_query + "\n<" + nation_uri + "> ont:isCitedIn <" + news + "> ."

            ##### DEEEP SCRAPING #####
            companies = news_pool[news]['companies']
            for company in companies:
                company_name = format_name(companies[company]['name'])
                market_name = format_name(companies[company]['market_index'][1:-1])
                # add triple about company type
                company_type = self.__lookuper.company_type_lookup(companies[company]['type'])
                if company_type is not None:
                    partial_query = partial_query + '\n<ont:' + company_name + '> rdf:type ont:' \
                                    + company_type + ', owl:NamedIndividual .'
                else:
                    # If the company is not found in the lookup (None), set it as OtherEntity
                    partial_query = partial_query + '\n<ont:' + company_name + '> rdf:type ont:' \
                                    + 'OtherEntity' + ', owl:NamedIndividual .'
                partial_query = partial_query + '\n<ont:' + company_name + '> rdfs:seeAlso <' \
                                + get_dbpedia_uri(company_name) + '> .'

                # add company stock name
                partial_query = partial_query + '\n<ont:' + company_name + '> ont:hasStockName: "' \
                                + company + '"^^xsd:string .'

                # add triples about market index
                # check if the market index of the company is already into the knowledge base, otherwise add it
                if self.__lookuper.market_index_lookup(companies[company]["market_index"]) is None:
                    partial_query = partial_query + '\n<ont:' + market_name + '>' \
                                    ' rdf:type ont:StockExchange, owl:NamedIndividual .'
                    self.__lookuper.update_table(False, market_name)
                    partial_query = partial_query + '\n<ont:' + market_name + '> rdfs:seeAlso <' \
                                    + get_dbpedia_uri(market_name) + '> .'
                # In both cases, retrieve correct uri from lookup
                partial_query = partial_query + '\n<ont:' + company_name + '> ont:isQuotedOn <' \
                                + self.__lookuper.market_index_lookup(companies[company]["market_index"]) + '> .'

                # add triples about company's ceo
                for ceo in companies[company]['ceo']:
                    ceo = format_name(ceo)
                    # verify if the system already knows this person, otherwise update it with a new individual
                    if self.__lookuper.person_lookup(ceo) is None:
                        partial_query = partial_query + '\n<ont:' + ceo + '> rdf:type ont:Person, ' \
                                        'owl:NamedIndividual .'
                        self.__lookuper.update_table(True, ceo, False)
                        partial_query = partial_query + '\n<ont:' + ceo + '> rdfs:seeAlso <' + get_dbpedia_uri(ceo) + '> .'
                    partial_query = partial_query + '\n<ont:' + company_name + '> ont:hasCEO <ont:'\
                                    + ceo + '> .'
                    partial_query = partial_query + '\n<ont:' + ceo + '> ont:isImportantPersonOf <ont:' + \
                                    company_name + '> .'

                # add triples about company location
                try:
                    place = companies[company]['site']
                    partial_query = partial_query + '\n<ont:' + company_name + '> ont:isLocatedIn ' \
                           '<http://www.bpiresearch.com/BPMO/2004/03/03/cdl/Countries#ISO3166.' + place + '> .'
                except KeyError:
                    print("No site took over for the company " + companies[company]['name'])

                # add triple about company citation in a news
                partial_query = partial_query + '\n<ont:' + company_name + '> ont:isCitedIn <' + news + '> .'

            # add triples about persons relevance for countries and organizations
            for person in person_list:
                for company in companies:
                        partial_query = partial_query + '\n<ont:' + person + '> ont:isImportantPersonOf <ont:' + \
                                        format_name(companies[company]['name']) + '> .'
            for person in person_list:
                for country in nation_list:
                    partial_query = partial_query + '\n<ont:' + person + '> ont:isImportantPersonOf <ont:' + \
                                    country + '> .'
        partial_query = partial_query + "\n}"
        #self.__db_manager.doUpdate(partial_query)
        print(partial_query)
        print()

    """ 
    Loads the individuals representing some of the most influential persons in the economics field and the most important
    stock exchange markets 
    @:return None
    """
    def load_persons_and_markets(self):
        partial_query = self.__query_prefix
        partial_query = partial_query + self.__insert_prefix
        for person in self.__lookuper.get_person_table():
            partial_query = partial_query + '\n<ont:' + format_name(person) + '> rdf:type ont:Person, owl:NamedIndividual .'
            partial_query = partial_query + '\n<ont:' + format_name(person) + '> rdfs:seeAlso <'+ get_dbpedia_uri(person) + '> .'
        for market in self.__lookuper.get_market_table():
            partial_query = partial_query + '\n<ont:' + market.replace(" ", "_") + '> rdf:type ont:StockExchange, owl:NamedIndividual .'
            partial_query = partial_query + '\n<ont:' + market.replace(" ", "_") + '> rdfs:seeAlso <' + get_dbpedia_uri(market) + '> .'
        partial_query = partial_query + "\n}"
        #self.__db_manager.doUpdate(partial_query)
        #print(partial_query)


if __name__ == "__main__":
    trp = Tripleizer()
    test_dict = {
    "http://feeds.reuters.com/~r/reuters/businessNews/~3/0iLYrt1zylE/coca-cola-chooses-plastic-bottle-collection-over-aluminum-cans-to-cut-carbon-footprint-idUSKBN1XG2J6": {
        "authors": "Alexis Akwagyiram;",
        "companies": {
            "KO.N": {
                "ceo": ["James R. Quincey"],
                "change": "(-0,17%)",
                "last_trade": "52,20USD",
                "market_index": " New York Stock Exchange ",
                "name": "Coca-Cola Co",
                "type": "Beverages (Nonalcoholic)"
            },
            "PEP.O": {
                "ceo": ["Ramon Laguarta", "Kirk C. Tanner", "Steven C. Williams", "Ram Krishnan"],
                "change": "(-0,55%)",
                "last_trade": "132,59USD",
                "market_index": " NASDAQ ",
                "name": "PepsiCo, Inc.",
                "type": "Beverages (Nonalcoholic)"
            }
        },
        "date": "2019-11-06T11:21:00+02:00",
        "text": "Coca-Cola chooses plastic bottle collection over aluminum cans to cut carbon footprint"
    },
    "http://feeds.reuters.com/~r/reuters/businessNews/~3/4MmtENHAslA/britains-virgin-media-switches-to-vodafones-mobile-network-idUSKBN1XG26L": {
        "authors": "Louise Heavens,",
        "companies": {
            "BT.L": {
                "ceo": [],
                "change": "(-1,71%)",
                "last_trade": "187,14GBP",
                "market_index": " London Stock Exchange (LON) ",
                "name": "BT Group plc",
                "type": "Software & Programming"
            },
            "LBTYA.O": {
                "ceo": ["Michael Thomas Fries"],
                "change": "(-0,12%)",
                "last_trade": "24,82USD",
                "market_index": " NASDAQ ",
                "name": "Liberty Global PLC",
                "type": "Broadcasting & Cable TV"
            },
            "TEF.MC": {
                "ceo": ["Jose Maria Alvarez-Pallete Lopez"],
                "change": "(-0,12%)",
                "last_trade": "6,86EUR",
                "market_index": " Mercado Continuo Espana ",
                "name": "Telefonica SA",
                "type": "Communications Services"
            }
        },
        "date": "2019-11-06T13:04:00+02:00",
        "text": "Britain's Virgin Media switches to Vodafone's mobile network"
        }
    }

    test_dict_ner = {
        "http://feeds.reuters.com/~r/reuters/businessNews/~3/0iLYrt1zylE/coca-cola-chooses-plastic-bottle-collection-over-aluminum-cans-to-cut-carbon-footprint-idUSKBN1XG2J6": {
            "authors": "Alexis Akwagyiram;",
            "companies": {
                "KO.N": {
                    "ceo": ["James R. Quincey"],
                    "change": "(-0,17%)",
                    "last_trade": "52,20USD",
                    "market_index": " New York Stock Exchange ",
                    "name": "Coca-Cola Co",
                    "type": "peppe"
                },
                "PEP.O": {
                    "ceo": ["Ramon Laguarta", "Kirk C. Tanner", "Steven C. Williams", "Ram Krishnan"],
                    "change": "(-0,55%)",
                    "last_trade": "132,59USD",
                    "market_index": " NASDAQ ",
                    "name": "PepsiCo, Inc.",
                    "type": "Beverages (Nonalcoholic)"
                }
            },
            "date": "2019-11-06T11:21:00+02:00",
            "text": "Elon Musk wants to invest in India, in the National Stock Exchange of India"
        },
    }

    trp.generate_insert(news_pool=test_dict_ner)

