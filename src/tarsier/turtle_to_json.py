from rdflib import Graph,URIRef,BNode

def turtle_to_json(turtle_text):
    with open("tmp", encoding="utf8",mode="w") as f:
        f.write(turtle_text)
        f.close()

    g = Graph()

    g.parse("tmp", format="turtle")

    result = {"head":{"vars":["s","p","o"]},"results":{"bindings":[]}}

    for stmt in g:
        type_ele = ["","",""]
        for i in range(3):
            if isinstance(stmt[i], URIRef):
                type_ele[i] = "uri"
            elif isinstance(stmt[i], BNode):
                type_ele[i] = "bnode"
            else:
                type_ele[i] = "literal"
        result["results"]["bindings"].append({"s": {"type": type_ele[0], "value": str(stmt[0])}, "p": {"type": type_ele[1], "value": str(stmt[1])},
         "o": {"type": type_ele[2], "value": str(stmt[2])}})

    return result



if __name__ == "__main__":
    turtle_to_json()



