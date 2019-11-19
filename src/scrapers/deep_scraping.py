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

def make_request(url,date = None,delay=5):
    triples = None
    auth = None
    if "reuters" in url or "bloomberg" in url:
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("headless")

            session = webdriver.Chrome(options=chrome_options)

            session.get(url)

            # Wait for the page
            response = session.page_source
            if "reuters" in url:
                myElem = WebDriverWait(session, delay).until(EC.presence_of_element_located((By.CLASS_NAME , 'Attribution_content')))
                triples,auth = scrape_reuters_request(session,response)
            elif "bloomberg" in url:
                myElem = WebDriverWait(session, delay).until(EC.presence_of_element_located((By.CLASS_NAME , 'lede-text-v2__container')))
                triples,auth = scrape_bloomberg_request(session,response)

            # Save info
            if date is not None:
                save_triples(url,auth,triples,filename = "news_"+str(date.year)+str(date.month)+str(date.day)+".json")

            response_obj = {"authors":auth,"companies":triples}

        except TimeoutException:
            visible_session = webdriver.Chrome()
            visible_session.get(url)
            input("CAPTCHA timeout. Press a key to continue...")
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

def scrape_reuters_request(session,text):
    print("Reuters request")

    # Getting authors
    authors_text = session.find_element_by_class_name("Attribution_content").text
    author = ' '.join(authors_text.split()[2:4])
    #print("author ",author)
    
    # Retrieve companies in the article
    corpus_text = session.find_element_by_class_name("StandardArticleBody_body")
    company_pages = []
    for p in corpus_text.find_elements_by_tag_name("p"):
        span = p.find_elements_by_tag_name("span")
        if len(span) > 0:
            a = span[0].find_elements_by_tag_name("a")
            if len(a) > 0:
                company_pages.append((a[0].text,a[0].get_attribute("href")))
    #print(company_pages)

    # Company pages scraping
    companies = {}
    for company,link in company_pages:
        companies[company] = {}
        
        try:
            session.get(link)

            # name
            companies[company]["name"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[1]/div[1]/h1').text
            
            # last_trade 
            companies[company]["last_trade"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/span[1]').text
            companies[company]["last_trade"] += session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[2]/span[2]').text
            
            # change
            companies[company]["change"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/div[3]/span[2]').text

            # Market index
            p = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[3]/div/div/div[1]/p').text

            p = re.sub(".* on the","",p)
            p = re.sub("∙ .*","",p)

            companies[company]["market_index"] = p

            # Type
            companies[company]["type"] = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[4]/div[2]/div/div[1]/div[1]/p[2]').text
            

            # CEO
            companies[company]["ceo"] = []
            about = session.find_element(By.XPATH,'//*[@id="__next"]/div/div[4]/div[1]/div/div/div/div[4]/div[2]/div/div[2]/div')
            for div in about.find_elements_by_tag_name("div"):
                p_container = div.find_elements_by_tag_name("p")
                if "Chief Executive Officer" in p_container[0].text:
                    companies[company]["ceo"].append(p_container[1].text)
                elif "Chief Executive Officer" in p_container[1].text:
                    companies[company]["ceo"].append(p_container[0].text)
        except:
            pass
            #print("Error retriving info")
    #print(author,repr(companies))
    return companies,author

def scrape_bloomberg_request(session,text):
    print("BLOOMBERG request")
    parser = BeautifulSoup(text, "html.parser")

    # Getting authors
    authors = parser.find_all("a",attrs={"rel":"author"})
    author = []
    for a in authors:
        author.append(a.text)

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
    #print("Company pages: ",company_pages)
    companies = {}
    for company,link in company_pages:
        companies[company] = {}
        
        try:
            session.get("https://www.bloomberg.com"+link)
            parser = BeautifulSoup(session.page_source, "html.parser")
            #print(session.current_url)
            
            if "quote" in session.current_url:
                # Name
                companies[company]["name"] = parser.find_all("h1",class_="companyName__99a4824b")[0].text
                #print("NAME ",companies[company]["name"])
                
                # Last_trade
                companies[company]["last_trade"] = ""
                last_trade_container = parser.find_all("div",class_="overviewRow__0956421f")[0]
                for span in last_trade_container.find_all("span"):
                    companies[company]["last_trade"] += span.text
                #print("LAST TRADE ",companies[company]["last_trade"])
                
                # Change
                span_change = parser.find_all("span",class_=re.compile("changePercent__2d7dc0d2 .*"))
                companies[company]["change"] = span_change[0].text
                
                #print("CHANGE ",companies[company]["change"])
                
                # Market index
                companies[company]["market_index"] = parser.find_all("span",class_="exchange__c62926ba")[0].text
                #print("MARKET INDEX ",companies[company]["market_index"])
                
                # Type
                companies[company]["type"] = parser.find_all("div",class_="industry labelText__6f58d7c0")[0].text
                #print("TYPE ",companies[company]["type"])
                
                # Site
                box = parser.find_all("section",class_="dataBox address")[0]
                companies[company]["site"] = box.find_all("div",class_="value__b93f12ea")[0].text
                #print("SITE ",companies[company]["site"])

            else:
                # Name
                companies[company]["name"] = parser.find_all("h1",class_="companyName__9bd88132")[0].text
                #print("NAME ",companies[company]["name"])
                
                # Type and Site
                container = parser.find_all("div",class_="infoTable__96162ad6")[0]
                for section in container.find_all("section"):
                    if section.h2.text == "SECTOR":
                        companies[company]["type"] = section.div.text
                    elif section.h2.text == "ADDRESS":
                        companies[company]["site"] = section.div.text

                companies[company]["market_index"] = None
                companies[company]["change"] = None
                companies[company]["last_trade"] = None
                
            
            # CEO
            container = parser.find_all("div",class_="executivesContainer__7f9fc250")[0]
            companies[company]["ceo"] = []
            for div in container.find_all("div",class_="info__368b37b6"):
                divin = div.find_all("div")
                if divin[0]["data-resource-type"]=="Person" and "CEO" in divin[1].text:
                    companies[company]["ceo"].append(divin[0].text)
            #print("CEO ",companies[company]["ceo"])
        except Exception as e:
            pass
            #print("Error retriving info: ", e)
                
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
