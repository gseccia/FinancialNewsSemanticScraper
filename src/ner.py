import paralleldots
import pprint

TOKEN = "zmxvDWsLaMuo6cxA1ZuIhjaqw6vtNVc9OVB5RgHQWFw"

'''
Result by paralleldots ner request example:
{'entities': 
    [{
    'name': 'french', 
    'category': 'place', 
    'confidence_score': 0.6469822526
    },
    {
    'name': 'europe', 
    'category': 'place', 
    'confidence_score': 0.9100195765
    }]
}
'''


def text_ner(text: str, confidence_threshold_pers: int = 0.35, confidence_threshold_plac: int = 0.35) -> list:
    """
    Asks paralleldots.ner to find persons and nations in the news title
    @:param news title as a string
    @:param confidence_threshold
    @:return list composed of dictionary of persons and places if found any
    Example
    [   {'name': 'france', 'category': 'place'},
        {'name': 'moon jae-in', 'category': 'name'},
        {'name': 'kazakhstan', 'category': 'place'}
    ]
    """
    text = text.lower()
    try:
        result_dict = paralleldots.ner(text)

        l = list()
        for el in result_dict['entities']:
            current_element = dict()
            if el['category'] == 'place' and el['confidence_score'] >= confidence_threshold_plac \
                    or el['category'] == 'name' and el['confidence_score'] >= confidence_threshold_pers:
                current_element['name'] = el['name']
                current_element['category'] = el['category']
                l.append(current_element)
        return l
    except Exception as e:
        print("Errore nel NER: ", e)
        return []

if __name__ == "__main__":
    # ATTENZIONE QUESTO VA INSERITO NELL'INIT DEL PROGRAMMA
    paralleldots.set_api_key(TOKEN)
    #
    r = text_ner("Moon Jae-in Opens Up for Foreign Investment, Spurring Rivalry With Kazakhstan")
    pprint.pprint(r)
