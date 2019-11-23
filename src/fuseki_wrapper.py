import subprocess
from SPARQLWrapper import SPARQLWrapper, JSON
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import os
import signal
import time
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class FusekiSparqlWrapper:

    def __init__(self, dataset_name: str = 'financial'):
        """
        :param dataset_name: name of the database
        """
        self.__set_update_endpoint(dataset_name)
        self.__set_query_endpoint(dataset_name)
        self.__update_wrapper()
        self.__dataset = dataset_name

    def __set_query_endpoint(self, dataset: str):
        """
        Set up the uri of the query endpoint of the database. Necessary to make queries.
        Must be called for each database you need to interrogate.
        :param dataset: name of the database
        """
        self.__query_endpoint = 'http://localhost:3030/' + dataset + '/query'

    def __set_update_endpoint(self, dataset: str):
        """
        Set up the uri of the update endpoint of the database. Necessary to make queries.
        Must be called for each database you need to interrogate.
        :param dataset: name of the database
        """
        self.__update_endpoint = 'http://localhost:3030/' + dataset + '/update'

    def __update_wrapper(self):
        """
        Set up SPARQLWrapper, it is based on the instances of the endpoints, so changing the name of the database
        requires different endpoints uri and a different instance of SPARQLWrapper.
        """
        self.__fuseki_query_wrapper = SPARQLWrapper(endpoint=self.__query_endpoint,
                                                    updateEndpoint=self.__update_endpoint)

    def doSelect(self, queryString: str):
        self.__fuseki_query_wrapper.setQuery(queryString)
        self.__fuseki_query_wrapper.method = 'POST'
        self.__fuseki_query_wrapper.setReturnFormat(JSON)
        results = self.__fuseki_query_wrapper.queryAndConvert()
        return results["results"]["bindings"]

    def doUpdate(self, queryString: str):
        self.__fuseki_query_wrapper.setQuery(queryString)
        self.__fuseki_query_wrapper.method = 'POST'
        self.__fuseki_query_wrapper.query()

    def start_fuseki(self, fuseki_location: str = "\\resources\\apache-jena-fuseki") -> int:
        """
        Execute Fuseki jar and returns PID of the process, necessary to shut down Fuseki by the program.
        """
        path = fuseki_location # str(Path(ROOT_DIR).parents[0]) + fuseki_location
        # subprocess.call(['java', '-jar', 'fuseki-server.jar'], cwd=path.replace("\\","/"))

        # Execute jar file
        process = subprocess.Popen(['java', '-jar', 'fuseki-server.jar'],
                                   creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                                   cwd=path.replace("\\", "/"),
                                   # Comment following line to use Fuseki verbose mode
                                   stderr=subprocess.PIPE, stdout=subprocess.PIPE
                                   )
        return process.pid

    def load_ontology(self):
        """
        Load ontology to the current dataset specified in the init.
        Location and name of the ontology is hardcoded but can be transferred to a parameter if needed.
        """
        multipart_data = MultipartEncoder(fields={'file': ('FinancialNewsOntology_beta3.owl',
                                                           open(
                                                               '../../resources/ontologies/FinancialNewsOntology_beta3.owl',
                                                               'rb'), 'text/plain')
                                                  })
        response = requests.put('http://localhost:3030/' + self.__dataset + '/data', data=multipart_data,
                                # auth=('admin', 'admin'),
                                headers={'Content-Type': multipart_data.content_type})
        response.raise_for_status()

    def stats_fuseki(self):
        """
        :return: Stats about the server
        """
        return requests.get('http://localhost:3030/$/stats/' + self.__dataset)

    def kill_fuseki(self, process_id):
        """
        :param process_id: process identifier
        :return: Fuseki process shut down
        """
        os.kill(process_id, signal.SIGTERM)

    def clear_graph(self):
        """
        Clear all triples in the current dataset.
        """
        # To specify a graph syntax is DROP GRAPH <URI_GRAPH>
        self.doUpdate("DROP DEFAULT")  # Or DROP ALL

    def delete_dataset_fuseki(self):
        """
        Delete the dataset whose name was chosen in the class init
        """
        res = requests.delete('http://localhost:3030/$/datasets/' + self.__dataset)
        print("Cancellation: ", res)

    def create_dataset_fuseki(self):
        """
        Create the dataset whose name was chosen in the class init
        """
        res = requests.post('http://localhost:3030/$/datasets', data={'dbName': self.__dataset, 'dbType': 'tdb'})
        print("Creation: ", res)


if __name__ == "__main__":
    # Example of usage

    # Initialize the wrapper choosing the dataset name
    wrapper = FusekiSparqlWrapper(dataset_name='koshka')
    # Execute Fuseki jar
    pid = wrapper.start_fuseki()
    print("Fuseki started with PID: ", pid)
    time.sleep(10)
    # Create the dataset requested
    wrapper.create_dataset_fuseki()
    time.sleep(10)
    # Load ontology in the dataset
    wrapper.load_ontology()
    print("Loaded ontology")
    time.sleep(20)

    # Clear graph ontology in the dataset
    wrapper.clear_graph()
    print("Cleared graph go check...")
    time.sleep(20)
    # Delete dataset
    wrapper.delete_dataset_fuseki()
    time.sleep(20)
    # Kill Fuseki process
    print("Killing Fuseki")
    wrapper.kill_fuseki(pid)
