from SPARQLWrapper import SPARQLWrapper, JSON


sparql = SPARQLWrapper("http://localhost:8890/sparql")

# For insert, update load ecc need to grant SPARQL_UPDATE privilege to SPARQL user
queryString = "INSERT DATA { GRAPH <http://example.com/> { 'b' a 'c'. } }" 
sparql.method = 'POST'
sparql.setReturnFormat(JSON)
results = sparql.query()


queryString = "CONSTRUCT { ?s ?p ?o } WHERE { ?s ?p ?o } LIMIT 200" 
sparql.method = 'GET'
sparql.setReturnFormat(JSON)
results = sparql.query().convert()


for result in results["results"]["bindings"]:
    print(result)