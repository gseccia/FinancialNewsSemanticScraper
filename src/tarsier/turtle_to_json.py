from rdflib import Graph,URIRef,BNode,Literal

def turtle_to_json(turtle_text):
    with open("tmp", encoding="utf8",mode="w") as f:
        f.write(turtle_text)
        f.close()

    g = Graph()

    g.parse("tmp", format="turtle")

    result = {"head":{"vars":["s","p","o"]},"results":{"bindings":[]}}

    for stmt in g:
        ref = ["s", "p", "o"]
        tmp_dict = {"s": {},
                    "p": {},
                    "o": {}}
        for i in range(3):
            if isinstance(stmt[i], URIRef):
                tmp_dict[ref[i]]["type"] = "uri"
            elif isinstance(stmt[i], BNode):
                tmp_dict[ref[i]]["type"]  = "bnode"
            else:
                tmp_dict[ref[i]]["type"]  = "literal"
                if stmt[i].datatype:
                    tmp_dict[ref[i]]["datatype"] = stmt[i].datatype
            tmp_dict[ref[i]]["value"] = stmt[i]

        result["results"]["bindings"].append(tmp_dict)

    return result



if __name__ == "__main__":
    turtle_to_json()



