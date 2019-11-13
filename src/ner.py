import paralleldots
import datetime
import csv
import json

TOKEN = "zmxvDWsLaMuo6cxA1ZuIhjaqw6vtNVc9OVB5RgHQWFw"


def news_ner(filename,date, count = 10):
    results = {}
    i = 0
    with open(filename,"r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date_row = datetime.datetime.strptime(row["date"],"%Y-%m-%dT%H:%M:%S+02:00")
            if date_row > date and i < count:
                text = row["text"].lower()
                results[row["link"]]=paralleldots.ner(text)
                results[row["link"]]["text"] = text
                i += 1
        f.close()
    return results


if __name__ == "__main__":
    paralleldots.set_api_key(TOKEN)
    date_limit = datetime.datetime.strptime("1970-01-01T00:00:00+02:00","%Y-%m-%dT%H:%M:%S+02:00")
    results = news_ner("news.csv",date_limit)
    with open("test.json","r") as f:
        news_elab = json.load(f)
        f.close()
        
    news_elab.update(results)
        
    with open("test.json","w") as f:
        f.write(json.dumps(news_elab))
        f.close()
