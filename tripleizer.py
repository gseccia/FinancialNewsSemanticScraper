import csv
import os.path
from fuseki_wrapper import FusekiSparqlWrapper
from topic_classifier import TopicClassifier
from brmapping import *
from fsanalysis import *


class Tripleizer():
    """ Class constructor """

    def __init__(self, news_pool_file: str = "news.csv"):
        self.__db_manager = FusekiSparqlWrapper()
        self.__topic_classifier = TopicClassifier()
        self.__news_pool_file = news_pool_file
        self.__news_data = None
        self.__news_pool = None
        self.__query_prefix = """
        PREFIX ont: <http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        """
        self.__insert_prefix = "INSERT DATA {"
        self.__delete_prefix = "DELETE DATA {"
        self.__analyser = FinancialSentimentAnalysis()

    """ 
    Setter method for companies data.
    @:param companies_data dictionary storing all the info about the cited companies in the news 
    @:return None
    """

    def set_companies_data(self, news_data: dict):
        self.__news_data = news_data

    """
    Generates an insert query for an RDF triples storage. 
    @:param source indicates whether the data is coming from Reuters or Bloomberg
    @:return string representing the insert query
    """

    def generate_insert(self):
        # as first operation generate an insert query using the news pool data
        partial_query = self.__query_prefix
        partial_query = partial_query + self.__insert_prefix

        # get the latest pool of news
        if os.path.exists(self.__news_pool_file):
            # get an iterator for the pool of news
            with open(self.__news_pool_file, "r") as f:
                news_pool = csv.DictReader(f)

                for row in news_pool:
                    datetime = row["date"]
                    news_title = row["text"]
                    news_link = row["link"]
                    news_source = row["source"]
                    partial_query = partial_query + "\n<" + news_link + "> rdf:type ont:News, owl:NamedIndividual ."
                    partial_query = partial_query + '\n<' + news_link + '> ont:hasTitle "' + news_title + '"^^xsd:string .'
                    partial_query = partial_query + '\n<' + news_link + '> ont:hasDateTime "' + datetime + '"^^xsd:string .'

                    # news topic is defined by the ML classifier
                    macro_topic, specific_topic = self.__topic_classifier.classify_news(news_title)
                    if macro_topic == "EconomicsTopic":
                        partial_query = partial_query + "\n<" + news_link + "> ont:hasEconomicsTopic ont:" + specific_topic + " ."
                    else:
                        partial_query = partial_query + "\n<" + news_link + "> ont:hasOtherTopic ont:" + specific_topic + " ."

                    # add news sentiment positiveness
                    t = self.__analyser.sentiment_analysis(news_title)
                    partial_query = partial_query + '\n<' + news_link + '> ont:hasPositivenessRank "' + \
                                    self.__analyser.sentiment_analysis(news_title) + '"^^xsd:float .'

                    if news_source == "B":
                        # news retrieved from Bloomberg
                        partial_query = partial_query + "\n<" + news_link + "> ont:publishedBy ont:Bloomberg ."
                    elif news_source == "R":
                        # news retrieved from Reuters
                        partial_query = partial_query + "\n<" + news_link + "> ont:publishedBy ont:Reuters ."
                    else:
                        # news retrieved from other publishers
                        partial_query = partial_query + "\n<" + news_link + "> ont:publishedBy ont:OtherPublisher ."
        partial_query = partial_query + "\n}"
        self.__db_manager.doUpdate(partial_query)
        print(partial_query)
        print()

        # generate insert query about news facts
        partial_query = self.__query_prefix
        partial_query = partial_query + self.__insert_prefix
        for news in self.__news_data:
            for author in self.__news_data[news]["author"]:
                partial_query = partial_query + '\nont:' + author + ' rdf:type ont:Person, owl:NamedIndividual .'
                partial_query = partial_query + '\n<' + news + '> ont:hasAuthor ont:' + author + ' .'

            companies = self.__news_data[news]['companies']
            for company in companies:
                company_type = self.company_type_lookup(company['type'])
                partial_query = partial_query + '\nont:"' + company[
                    'name'] + '" rdf:type ont:"' + company_type + '", owl:NamedIndividual .'
                partial_query = partial_query + '\nont:"' + company[
                    'market_index'] + '" rdf:type ont:MarketIndex, owl:NamedIndividual .'
                partial_query = partial_query + '\nont:"' + company['name'] + '" ont:isQuotedOn ont:"' + company[
                    'market_index'] + '" .'
                for ceo in company['ceo']:
                    partial_query = partial_query + '\nont:"' + ceo + '" rdf:type ont:Person, owl:NamedIndividual .'
                    partial_query = partial_query + '\nont:"' + company[
                        'name'] + '" ont:hasChairman/CEO ont:"' + ceo + '" .'
                if company['site'] is not None:
                    partial_query = partial_query + '\nont:"' + company['name'] + '" ont:hasSite ont:"' + company['site'] + '" .'
                partial_query = partial_query + '\nont:"' + company['name'] + '" ont:isCitedIn ont:<' + news + '> .'
        partial_query = partial_query + "\n}"
        self.__db_manager.doUpdate(partial_query)
        print(partial_query)
        print()

    """ 
    Generates an update query for an RDF triples storage. 
    @:param source indicates whether the data is coming from Reuters or Bloomberg
    @:return string representing the update query
    
    Update queries are necessary because some pieces of information in the ontology can change during time, for example
    the value of some stocks, the CEO of a company etc. Update queries are implemented as DELETE+INSERT
    """

    def generate_update(self):
        # firstly delete the triples that have to be updated
        partial_query_delete = self.__query_prefix
        partial_query_insert = self.__query_prefix
        partial_query_delete = partial_query_delete + self.__delete_prefix
        partial_query_insert = partial_query_insert + self.__insert_prefix
        for news in self.__news_data:
            companies = self.__news_data[news]["companies"]
            for company in companies:
                partial_query_delete = partial_query_delete + "\nont:" + company["name"] + " ont:hasMarketValue ?value"
                partial_query_delete = partial_query_delete + "\nont:" + company[
                    "name"] + " ont:hasPercentageVariation ?value"
                partial_query_insert = partial_query_insert + "\nont:" + company["name"] + " ont:hasMarketValue " + \
                                       company["last_trade"] + "^^xsd:float"
                partial_query_insert = partial_query_insert + "\nont:" + company[
                    "name"] + " ont:hasPercentageVariation " + \
                                       company["change"] + "xsd:float"
        partial_query_delete = partial_query_delete + "\n}"
        partial_query_insert = partial_query_insert + "\n}"
        self.__db_manager.doUpdate(partial_query_delete)
        self.__db_manager.doUpdate(partial_query_insert)
        print(partial_query_delete)
        print()
        print(partial_query_insert)
        print()

    def company_type_lookup(self, cat: str) -> str:
        return remove_whitespaces(br_classes[cat])


if __name__ == "__main__":
    trp = Tripleizer('news_test.csv')
    test_dict = {
    'https://www.bloomberg.com//news/articles/2019-11-06/french-economic-renaissance-gives-europe-new-engine-for-growth?srnd=markets-vp':
        {
            'author': ['Antonio Vicinanza'],
            'companies':
                [
                {
                    'name': 'Dell Technologies Inc',
                    'last_trade': '54,33USD',
                    'site': 'France',
                    'change': '(-0,18%)',
                    'market_index': 'New York Stock Exchange',
                    'type': 'Computer & Electronics Retailers',
                    'ceo': ['Michael S. Dell']
                }
                ]
        }
    }

    trp.set_companies_data(test_dict)
    trp.generate_insert()
    # trp.generate_update()

