from typing import Tuple
from SPARQLWrapper import SPARQLWrapper, JSON


class FusekiSparqlWrapper():

    def __init__(self, query_endpoint:str='http://localhost:3030/financial/query',
                        update_endpoint:str='http://localhost:3030/financial/update'):
        self.__query_endpoint = query_endpoint
        self.__update_endpoint = update_endpoint
        self.__fuseki_query_wrapper = SPARQLWrapper(endpoint=self.__query_endpoint,updateEndpoint=self.__update_endpoint)
        #print(self.__fuseki_query_wrapper)
        #self.__fuseki_update_wrapper = SPARQLWrapper(self.__update_endpoint)
            
    def doSelect(self, queryString:str):
        self.__fuseki_query_wrapper.setQuery(queryString)
        self.__fuseki_query_wrapper.method = 'POST'
        self.__fuseki_query_wrapper.setReturnFormat(JSON)
        results = self.__fuseki_query_wrapper.queryAndConvert()
        return results["results"]["bindings"]
    
    def doUpdate(self, queryString:str):
        self.__fuseki_query_wrapper.setQuery(queryString)
        self.__fuseki_query_wrapper.method = 'POST'
        self.__fuseki_query_wrapper.query()


"""

SPARQLStore non supporta i blank nodes e quindi non va bene questa soluzione

from rdflib import Graph, Literal, URIRef, BNode
from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore

def make_fuseki_graph_store(query_endpoint:str='http://localhost:3030/demo_financial/query',
                            update_endpoint:str='http://localhost:3030/demo_financial/update'):
    fuseki_store = SPARQLUpdateStore(queryEndpoint=query_endpoint, update_endpoint=update_endpoint)
    fuseki_store.open((query_endpoint, update_endpoint))

    #...use store...
    g = Graph(store=fuseki_store)
    return g
"""

if __name__ == "__main__":
    import logging
    import rdflib
    from rdflib.plugins.stores.sparqlstore import SPARQLUpdateStore
    import time

    logging.basicConfig()
    logger = logging.getLogger('logger')
    #logger.warning('The system may break down')

    start_time = time.time()

    fuseki_wrapper = FusekiSparqlWrapper()
    
    query = """
    select distinct ?s ?p ?o
    where { ?s ?p ?o}
            LIMIT 10
            """

    results = fuseki_wrapper.doSelect(queryString=query)
    for result in results:
        print(result)
        print()
    
    insertQuery = """
    PREFIX prova:<http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    INSERT DATA
    { 
    <https://www.amazon.it> rdf:type prova:ConsumerDiscretionary .
    }
    """

    deleteQuery = """
    PREFIX prova: <http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    DELETE DATA
    {
        <https://www.amazon.it> rdf:type prova:ConsumerDiscretionary .
    }
    """
    
    selectQuery = """
    PREFIX prova:<http://www.github.com/gseccia/FinancialNewsSemanticScraper/ontologies/FinancialNewsOntology>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select distinct ?s 
    where { ?s rdf:type prova:ConsumerDiscretionary .}
    """
    
    fuseki_wrapper.doUpdate(queryString=insertQuery)

    print("AFTER INSERT")
    results = fuseki_wrapper.doSelect(queryString=selectQuery)
    for result in results:
        print(result)
        print()
    

    fuseki_wrapper.doUpdate(queryString=deleteQuery)

    print("AFTER DELETE")
    results = fuseki_wrapper.doSelect(queryString=selectQuery)
    for result in results:
        print(result)
        print()

    print("--- %s seconds ---" % (time.time() - start_time))

