from bs4 import BeautifulSoup
import requests
from datetime import date


def retrieve_news(news_URL = "https://finviz.com/news.ashx"):
    """ Returns a list of news or None if there aren't """
    request = requests.get(news_URL)
    if request.status_code == 200:
        parser = BeautifulSoup(request.text, "html.parser")
        # Select only NEWS from table and ignore BLOGS
        news = parser.find_all("div", class_="news")[0].findChildren()[1].findChildren("tr", recursive=False)[1].\
            findChildren("td", recursive=False)[0].findChildren("a", class_="nn-tab-link")
        return list(map(lambda elem: elem.text,news))
    else:
        return None


if __name__ == "__main__":
    news = retrieve_news()

    with open("news" + date.today().strftime("%d%m%Y") + ".txt", "w") as f:
        for n in news:
            f.write(n+"\n")
        f.close()
