from bs4 import BeautifulSoup
import requests

def retrive_news(news_URL = "https://finviz.com/news.ashx"):
    """ Returns a list of news or None if there aren't """
    request = requests.get(news_URL)
    if request.status_code == 200:
        parser = BeautifulSoup(request.text, "html.parser")
        news = parser.find_all("a", class_="nn-tab-link") 
        news = news[1:] #first one is the title
        return list(map(lambda elem: elem.text,news))
    else:
        return None


if __name__=="__main__":
    news = retrive_news()

    with open("news.txt","w") as f:
        for n in news:
            f.write(n+"\n")
        f.close()
        
