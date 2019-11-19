#!/usr/bin/python3

# reqs
import pdb
import json
import requests
import traceback

from SPARQLWrapper import SPARQLWrapper, JSON #per la pezza

def doQuery(endpoint, q):

    # read input
    uri = endpoint["url"]
    query = endpoint["queryPrefix"]    
    headers = endpoint["httpHeaders"]
    verb = endpoint["httpVerb"]

    # manipulate input query
    try:
        
        finalQuery = json.loads(endpoint["queryPrefix"])
        finalQuery["query"] = q
        
    except:
        #print(traceback.print_exc())
        print("Query is simple string")
        finalQuery = endpoint["queryPrefix"] % q
    
    # manipulate input headers
    try:
        finalHeaders = json.loads(headers)
    except:
        finalHeaders = headers
        
    # HTTP POST
    if verb == "POST":
        try:
            
            print(uri)
            print(type(finalQuery))
            print(headers)
            print(finalQuery)
            r = requests.post(uri, data = finalQuery, headers = finalHeaders)
            #print(r.content.decode('UTF-8'))
            
        except:
            return False, None

    # HTTP GET
    else:
        try:
            payload = {'query': q, 'format':'json'}
            r = requests.get(uri, params = payload, headers = headers)
            print(r.url)
        except:
            return False, None

    # return
    try:
        res = json.loads(r.text)
        #print(res)
        return True, res
    except:
        return False, None
