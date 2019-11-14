import os.path
from fuseki_wrapper import FusekiSparqlWrapper
from topic_classifier import TopicClassifier
from fsanalysis import *
import json
import requests
from info_lookup import *
from utils import get_dbpedia_uri


class Tripleizer():
    """ Class constructor """

    def __init__(self):
        self.__db_manager = FusekiSparqlWrapper()
        self.__topic_classifier = TopicClassifier()
        self.__query_prefix = """
        PREFIX ont: <http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        """
        self.__insert_prefix = "INSERT DATA {"
        self.__delete_prefix = "DELETE DATA {"
        self.__analyser = FinancialSentimentAnalysis()
        self.__lookuper = InfoLookup()

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
            news_source = news_pool[news]["source"]
            partial_query = partial_query + "\n<" + news + "> rdf:type ont:News, owl:NamedIndividual ."
            partial_query = partial_query + '\n<' + news + '> ont:hasTitle "' + news_title + '"^^xsd:string .'
            partial_query = partial_query + '\n<' + news + '> ont:hasDateTime "' + datetime + '"^^xsd:dateTime .'

            # news topic is defined by the ML classifier
            macro_topic, specific_topic = self.__topic_classifier.classify_news(news_title)
            if macro_topic == "EconomicsTopic":
                partial_query = partial_query + "\n<" + news + "> ont:hasEconomicsTopic ont:" + specific_topic + " ."
            else:
                partial_query = partial_query + "\n<" + news + "> ont:hasOtherTopic ont:" + specific_topic + " ."

            # add news sentiment positiveness
            partial_query = partial_query + '\n<' + news + '> ont:hasPositivenessRank "' + \
                            self.__analyser.sentiment_analysis(news_title) + '"^^xsd:float .'

            if news_source == "B":
                # news retrieved from Bloomberg
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <" + get_dbpedia_uri('Bloomberg_News') + "> ."
            elif news_source == "R":
                # news retrieved from Reuters
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <" + get_dbpedia_uri('Reuters') + "> ."
            else:
                # news retrieved from other publishers
                partial_query = partial_query + "\n<" + news + "> ont:publishedBy <" + get_dbpedia_uri('News_agency') + "> ."

            # get info about persons cited in the news title
            # get info about market indices cited in the news title
            # get info about nations cited in the news title
            person_uri, market_uri, nation_uri = self.__lookuper.lookup(news_title)

            if person_uri is not None:
                partial_query = partial_query + "\n<" + person_uri + "> ont:isCitedIn <" + news + "> ."

            if market_uri is not None:
                partial_query = partial_query + "\n<" + market_uri + "> ont:isCitedIn <" + news + "> ."

            if nation_uri is not None:
                partial_query = partial_query + "\n<" + nation_uri + "> ont:isCitedIn <" + news + "> ."

        # partial_query = partial_query + "\n}"
        # self.__db_manager.doUpdate(partial_query)
        # print(partial_query)
        # print()

        ##### DEEEP SCRAPING #####
        # generate insert query about companies facts
        # partial_query = self.__query_prefix
        # partial_query = partial_query + self.__insert_prefix
        # for news in news_pool:
            companies = news_pool[news]['companies']
            for company in companies:

                # add triple about company type
                company_type = self.__lookuper.company_type_lookup(company['type'])
                # look for the company in dbpedia (?), otherwise create a new customized individual in the ontology
                partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> rdf:type ont:' \
                                + company_type + ', owl:NamedIndividual .'

                # add company stock name
                partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> ont:hasStockName:' \
                                + company + ' .'

                # add triples about market index
                # check if the market index of the company is already into the knowledge base, otherwise add it
                if self.__lookuper.market_index_lookup(company["market_index"]) is None:
                    partial_query = partial_query + '\n<' + get_dbpedia_uri(company['market_index']) + '>' \
                                    ' rdf:type ont:MarketIndex, owl:NamedIndividual .'
                    # IN PIU AGGIUNGI NELLA TABELLA DI LOOKUP
                partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> ont:isQuotedOn <' \
                                + get_dbpedia_uri(company['market_index']) + '> .'

                # add triples about company's ceo
                for ceo in company['ceo']:
                    # verify if the system already knows this person, otherwise update it with a new individual
                    if self.__lookuper.person_lookup(None, ceo) is None:
                        partial_query = partial_query + '\n<' + get_dbpedia_uri(ceo) + '> rdf:type ont:Person, ' \
                                        'owl:NamedIndividual .'
                        # IN PIU AGGIUNGI NELLA TABELLA DI LOOKUP
                    partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> ont:hasCEO <'\
                                    + get_dbpedia_uri(ceo) + '> .'

                # add triples about company location
                if company['site'] is not None:
                    partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> ont:isLocatedIn ' \
                           '<http://www.bpiresearch.com/BPMO/2004/03/03/cdl/Countries#ISO3166.' + company['site'] + '> .'

                # add triple about company citation in a news
                partial_query = partial_query + '\n<' + get_dbpedia_uri(company['name']) + '> ont:isCitedIn <' + news + '> .'
        partial_query = partial_query + "\n}"
        self.__db_manager.doUpdate(partial_query)
        print('Ok query done')
        # print(partial_query)
        print()

    """ 
    Loads the individuals representing some of the most influential persons in the economics field 
    @:param person_filename indicates the file in which data is stored
    @:return None
    """
    def load_persons(self, persons_filename: str = "vips.json"):
        with open(persons_filename, encoding="UTF-8") as json_file:
            persons = json.load(json_file)
        partial_query = self.__query_prefix
        partial_query = partial_query + self.__insert_prefix
        for person in persons:
            partial_query = partial_query+"\n<"+persons[person]["uri"]+"> rdf:type ont:Person, owl:NamedIndividual ."
        partial_query = partial_query + "\n}"
        self.__db_manager.doUpdate(partial_query)


    """
    Looks for some concept on DBPedia semantic database.
    @:param concept concept to look for
    @:return true if the concept is found, false otherwise
    
    The assumption is that dbpedia exposes concepts using the format dbpedia.org/page/concept
    """
    def ask_concept(concept: str) -> bool:
        # ATTENZIONE VANNO GESTITI ERRORI ED ECCEZIONI
        req = requests.get("http://dbpedia.org/page/" + concept)
        if req.status_code == 200:
            return True
        else:
            return False


if __name__ == "__main__":
    trp = Tripleizer()
    test_dict = {
    'https://www.bloomberg.com//news/articles/2019-11-06/french-economic-renaissance-gives-europe-new-engine-for-growth?srnd=markets-vp':
        {
            'date': '2019-11-04T23:00:00',
            'text': 'Hedge Funds Flock to Support Johnson, Fueled by Fears of Corbyn',
            'source': 'B',
            'author': ['Antonio Vicinanza'],
            'companies':
                [
                {
                    'name': 'Dell Technologies Inc',
                    'site': 'France',
                    'market_index': 'New York Stock Exchange',
                    'type': 'Computer & Electronics Retailers',
                    'ceo': ['Michael S. Dell']
                }
                ]
        }
    }

    trp.generate_insert(news_pool=test_dict)

