import json
import os
from bs4 import BeautifulSoup
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re
import datetime
import time

def make_request(url,exe_path,date = None,delay=10,verbose=False):
    triples = None
    auth = None
    if "reuters" in url or "bloomberg" in url:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")

        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
        chrome_options.add_argument('accept-language="it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"')

        if "reuters" in url:
            session = webdriver.Chrome(options=chrome_options, executable_path=exe_path+"chromedriver.exe")
        elif "bloomberg" in url:
            session = webdriver.Chrome(options=chrome_options,executable_path=exe_path+"chromedriver.exe")
        else:
            session = webdriver.Chrome(options=chrome_options, executable_path=exe_path+"chromedriver.exe")
        try:
            if verbose:
                print("Make a request to ",url)
            session.get(url)

            # Wait for the page
            response = session.page_source
            if "reuters" in url:
                myElem = WebDriverWait(session, delay).until(EC.presence_of_element_located((By.CLASS_NAME , 'Attribution_content')))
                triples,auth = scrape_reuters_request(session,response,verbose=verbose)
            elif "bloomberg" in url:
                myElem = WebDriverWait(session, delay).until(EC.presence_of_element_located((By.CLASS_NAME , 'lede-text-v2__hed')))
                triples,auth = scrape_bloomberg_request(session,response,exe_path,verbose=verbose)

            # Save info
            if date is not None:
                save_triples(url,auth,triples,filename = "news_"+str(date.year)+str(date.month)+str(date.day)+".json")

            response_obj = {"authors":auth,"companies":triples}

        except TimeoutException:
            if verbose:
                print("Timeout ==> Solve the captcha")
            visible_session = webdriver.Chrome(executable_path=exe_path+"chromedriver.exe")
            visible_session.get(url)
            # input("CAPTCHA timeout. Press a key to continue...")
            time.sleep(60)
            visible_session.close()
            visible_session.quit()
            response_obj = None

        finally:
            session.close()
            session.quit()
    else:
        response_obj = {}
    return response_obj


def save_triples(url,auth,triples,filename="triples.json"):
    
    if os.path.exists(filename):
        with open(filename,mode="r") as f:
            saved_triples = json.load(f)
            f.close()

        saved_triples[url] = {"authors":auth,"companies":triples}
        saved_triples["last"] = url
    else:
        saved_triples = {}
        saved_triples[url] = {"authors":auth,"companies":triples}
        saved_triples["last"] = url
    
    with open(filename,mode="w") as f:
        f.write(json.dumps(saved_triples))
        f.close()

def scrape_reuters_request(session,text,verbose = False):
    if verbose:
        print("*** Reuters Request ***")

    # Getting authors
    authors_text = session.find_element_by_class_name("Attribution_content").text
    author = ' '.join(authors_text.split()[2:4])

    # if verbose:
    #     print("author ",author)
    
    # Retrieve companies in the article
    corpus_text = session.find_element_by_class_name("StandardArticleBody_body")
    company_pages = []
    for p in corpus_text.find_elements_by_tag_name("p"):
        span = p.find_elements_by_tag_name("span")
        if len(span) > 0:
            a = span[0].find_elements_by_tag_name("a")
            if len(a) > 0:
                company_pages.append((a[0].text,a[0].get_attribute("href")))
    if verbose:
        print("Company pages: ",company_pages)
        if len(company_pages) > 0:
            print("Starting companies scraping")

    # Company pages scraping
    companies = {}
    for company,link in company_pages:
        companies[company] = {}

        try:
            session.get(link)
            try:
                element = session.find_element(By.XPATH, '// *[ @ id = "__next"] / div / h2[1]')
                if element is not None and element.text == "404":
                    del companies[company]
                    if verbose:
                        print("Page 404")
                else:
                    print("???")
            except:
                # name
                companies[company]["name"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div[1]/h1').text
                if verbose:
                    print("Company name: ",companies[company]["name"])

                # last_trade
                try:
                    companies[company]["last_trade"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/span[1]').text
                    companies[company]["last_trade"] += session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/span[2]').text
                except:
                    pass
                # if verbose:
                #     print("last_trade ",companies[company]["last_trade"])

                # change
                try:
                    companies[company]["change"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[3]/span[2]').text
                except:
                    pass
                # if verbose:
                #     print("change ",companies[company]["change"])

                # Market index
                try:
                    p = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/p').text

                    p = re.sub(".* on the","",p)
                    p = re.sub("∙ .*","",p)

                    companies[company]["market_index"] = p
                    if verbose:
                        print("Market index: ",companies[company]["market_index"])
                except:
                    if verbose:
                        print("Market index: not found")
                # Type
                try:
                    companies[company]["type"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[4]/div[2]/div/div[1]/div[1]/p[2]').text
                    if verbose:
                        print("Company type: ",companies[company]["type"])
                except:
                    if verbose:
                        print("Company type: not found")

                # CEO
                companies[company]["ceo"] = []
                try:
                    about = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[4]/div[2]/div/div[2]/div')
                    for div in about.find_elements_by_tag_name("div"):
                        p_container = div.find_elements_by_tag_name("p")
                        if "Chief Executive Officer" in p_container[0].text:
                            companies[company]["ceo"].append(p_container[1].text)
                        elif "Chief Executive Officer" in p_container[1].text:
                            companies[company]["ceo"].append(p_container[0].text)

                    if verbose:
                        print("CEO: ",companies[company]["ceo"])
                except:
                    if verbose:
                        print("CEO: not found")
        except Exception as e:
            if verbose:
                print("Error retrieving info ",e)
    if verbose:
        print("*** End Reuters Request ***")
    return companies,author

def scrape_bloomberg_request(session,text,exe_path,verbose = False):
    if verbose:
        print("*** Bloomberg request ***")
    parser = BeautifulSoup(text, "html.parser")
    # Getting authors
    authors = parser.find_all("a",attrs={"rel":"author"})
    author = []
    for a in authors:
        author.append(a.text)
    # if verbose:
    #     print("author ",author)

    # Retrieve companies in the article
    corpus_text = parser.find_all("div", class_="body-copy-v2 fence-body")[0]
    company_pages = []
    for p in corpus_text.find_all("p"):
        if p.a is not None and p.a.has_attr("title") and(p.a["title"] == "Price Graph" or p.a["title"] == "Company Overview"):
            #print(p.a,p.a["title"])
            company_name = re.sub(".*quote/","",p.a["href"])
            #print(company_name)
            company_pages.append((company_name,p.a["href"]))

    # Company pages scraping
    if verbose:
        print("Company pages: ", company_pages)
    companies = {}
    it = iter(company_pages)
    error = False
    force_next = 0
    if verbose:
        if len(company_pages) > 0:
            print("Starting companies scraping")
    while True:
        try:
            company,link = (company,link) if (error and force_next < 10) else next(it)
            if verbose and error:
                print("Retry to get ", link)
            error = False
            companies[company] = {}

            try:
                session.get("https://www.bloomberg.com"+link)

                parser = BeautifulSoup(session.page_source, "html.parser")
                if verbose:
                    print("Title page: ",parser.title.text)
                if "404 - Bloomberg" in parser.title.text:
                    del companies[company]
                    if verbose:
                        print("FOUND 404 - page")
                else:
                    force_next = 0
                    if "quote" in session.current_url:
                        myElem = WebDriverWait(session, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'companyName__99a4824b')))
                        # if verbose:
                        #     print("Quote type url parsing")
                        # Name
                        companies[company]["name"] = parser.find_all("h1",class_="companyName__99a4824b")[0].text
                        if verbose:
                            print("Company name: ",companies[company]["name"])

                        # Last_trade
                        last_trade_containers = parser.find_all("div",class_="overviewRow__0956421f")
                        if len(last_trade_containers) > 0:
                            companies[company]["last_trade"] = ""
                            last_trade_container = last_trade_containers[0]
                            for span in last_trade_container.find_all("span"):
                                companies[company]["last_trade"] += span.text
                        # if verbose:
                        #     if "last_trade" in companies[company]:
                        #         print("LAST TRADE ",companies[company]["last_trade"])
                        #     else:
                        #         print("LAST TRADE EMPTY")

                        # Change
                        span_change = parser.find_all("span", class_=re.compile("changePercent__2d7dc0d2 .*"))
                        if len(span_change) > 0:
                            companies[company]["change"] = span_change[0].text
                        # if verbose:
                        #     if "change" in companies[company]:
                        #         print("change ", companies[company]["change"])
                        #     else:
                        #         print("change EMPTY")

                        # Market index
                        market_index_container = parser.find_all("span", class_="exchange__c62926ba")
                        if len(market_index_container)>0:
                            companies[company]["market_index"] = market_index_container[0].text
                        if verbose:
                            if "market_index" in companies[company]:
                                print("Market index: ", companies[company]["market_index"])
                            else:
                                print("Market index is empty")

                        # Type
                        type_container = parser.find_all("div",class_="industry labelText__6f58d7c0")
                        if len(type_container) > 0:
                            companies[company]["type"] = type_container[0].text
                        if verbose:
                            if "type" in companies[company]:
                                print("Company type: ", companies[company]["type"])
                            else:
                                print("Company type is empty")

                        # Site
                        boxs = parser.find_all("section",class_="dataBox address")
                        if len(boxs)>0:
                            box = boxs[0]
                            companies[company]["site"] = box.find_all("div",class_="value__b93f12ea")[0].text
                        if verbose:
                            if "site" in companies[company]:
                                print("Company site: ", companies[company]["site"])
                            else:
                                print("Company site is empty")

                        # CEO
                        containers = parser.find_all("div", class_="executivesContainer__7f9fc250")
                        companies[company]["ceo"] = []
                        if len(containers)>0:
                            container = containers[0]
                            for div in container.find_all("div", class_="info__368b37b6"):
                                divin = div.find_all("div")
                                if divin[0]["data-resource-type"] == "Person" and ("CEO" in divin[1].text or "Chairman" in divin[1].text):
                                    companies[company]["ceo"].append(divin[0].text)
                        if verbose:
                            if "ceo" in companies[company]:
                                print("CEO: ", companies[company]["ceo"])
                            else:
                                print("CEO is empty")
                    else:
                        myElem = WebDriverWait(session, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'companyName__9bd88132')))
                        # if verbose:
                        #     print("Scraping NOT a quote page")
                        # Name
                        companies[company]["name"] = parser.find_all("h1",class_="companyName__9bd88132")[0].text
                        if verbose:
                            if "name" in companies[company]:
                                print("Namw: ", companies[company]["name"])
                            else:
                                print("Name is empty")

                        # Type and Site
                        containers = parser.find_all("div",class_="infoTable__96162ad6")
                        if len(containers) > 0:
                            container = containers[0]
                            for section in container.find_all("section"):
                                if section.h2.text == "SECTOR":
                                    companies[company]["type"] = section.div.text
                                elif section.h2.text == "ADDRESS":
                                    companies[company]["site"] = section.div.text
                        if verbose:
                            if "type" in companies[company]:
                                print("Company type: ", companies[company]["type"])
                            else:
                                print("Company type is empty")
                            if "site" in companies[company]:
                                print("Company site: ", companies[company]["site"])
                            else:
                                print("Company site is empty")

                        # companies[company]["market_index"] = "Empty"
                        # companies[company]["change"] = "Empty"
                        # companies[company]["last_trade"] = "Empty"
                        companies[company]["ceo"] = []

            except TimeoutException:
                if verbose:
                    print("Timeout ==>  Solve the captcha")
                visible_session = webdriver.Chrome(executable_path=exe_path + "chromedriver.exe")
                visible_session.get("https://www.bloomberg.com"+link)
                # input("CAPTCHA timeout. Press a key to continue...")
                time.sleep(60)
                visible_session.close()
                visible_session.quit()
                force_next += 1
                error = True
                #print("Error retriving info: ", e)
        except StopIteration:
            break
    # print(author,repr(companies))
    return companies,author

def save_file(new_file):
    # Save the news with author
    newfile = not os.path.exists("news_defintive.csv")
    with open("news_defintive.csv","a+")  as csv_file:
                fieldnames = ['date', 'text', 'link','authors']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames,dialect="excel")
                if newfile:
                    writer.writeheader()
                for row in new_file:
                    writer.writerow(row)
                csv_file.close()


if __name__ == "__main__":
    print(make_request("https://www.reuters.com/article/us-cannabis-stocks-europe/wave-of-european-cannabis-firms-to-list-in-2020-analyst-says-idUSKBN1Y21WS?feedType=RSS&feedName=businessNews&utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+reuters%2FbusinessNews+%28Business+News%29","./",verbose=True))
    """
    new_file = []
    filename = "news_2019119.json"
    select_news = False
    with open(filename,mode="r") as f:
        saved_triples = json.load(f)
        last_url = saved_triples["last"]
        f.close()
    selected_date = datetime.datetime.strptime("2019-11-11 00:00:00","%Y-%m-%d %H:%M:%S")
    
    if os.path.exists("news.csv"):
        # Get the news
        with open("news.csv","r") as f:
            csv_reader = csv.DictReader(f,dialect="excel")
            for row in csv_reader:
                date_row = datetime.datetime.strptime(row["date"],"%Y-%m-%dT%H:%M:%S+02:00")

                # row["link"]==last_url date_row > selected_date
                if date_row > selected_date and not select_news:
                    select_news = True

                if "authors" in row and select_news:
                    make_request(row["link"],date_row)
            f.close()
    else:
        print("No news")
    """
