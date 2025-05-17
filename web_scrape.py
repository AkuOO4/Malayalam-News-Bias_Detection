from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from csv import writer
from tqdm import tqdm


def get_all_links(url):
    time.sleep(1)
    
    links = set()
    body = driver.find_element(By.TAG_NAME, "body")
    
    # Scroll quickly to the bottom
    for _ in range(40):  # Adjust the range if needed
        body.send_keys(Keys.ARROW_DOWN)
    
    elements = driver.find_elements(By.TAG_NAME, "a")
    links.update(element.get_attribute("href") for element in elements if element.get_attribute("href") and element.get_attribute("href").startswith(url))
    
    
    return links

def news_scroll_repeat(linkin, url, paper, repetation = 50):
    driver.get(linkin)
    for i in tqdm(range(repetation), desc="repetation") :  
        try:

            
            links = get_all_links(url)
            with open(paper+".txt", "a") as f:
                for link in links:
                    f.write(link + "\n")
            print("---- ",paper,"-No. of URLs ----", len(links))

        
        except Exception as e:      
            #     current time, repetation number, error     
            log = [time.localtime(), i, e]
            with open('logs.csv', 'a') as f_object:    
                writer_object = writer(f_object)
                writer_object.writerow(log)          
                f_object.close()

def go_through_diff_site(details):
    for detail in tqdm(details,desc= "sites"):
        news_scroll_repeat(detail["linkin"], detail["website"],detail["paper"])
        time.sleep(10)

# url = "https://linkin.bio/deshabhimanionline"
details = [#{"paper":"deshabhimani", "linkin": "https://linkin.bio/deshabhimanionline", "website":"https://www.deshabhimani.com"},
           #{"paper":"manorama_news", "linkin": "https://linkin.bio/manoramanews/", "website":"https://www.manoramanews.com/"},
           #{"paper":"asianet_news", "linkin": "https://linkin.bio/asianetnews/", "website":"https://www.asianetnews.com/"},
            # {"paper":"true_Copy", "linkin": "https://linkin.bio/truecopythink/", "website":"https://truecopythink.media/"},
            {"paper":"reporter", "linkin": "https://linkin.bio/reportertv", "website":"https://www.reporterlive.com/"},
            {"paper":"veeekshanam", "linkin": "https://veekshanam.com/", "website":"https://veekshanam.com"},
            {"paper":"mathrubhumi", "linkin": "https://reead.in/mathrubhumi/?fbclid=PAY2xjawIuR5FleHRuA2FlbQIxMQABpqEcpd4EZFv2jG8vn1iAYWxKEZs5TX0z0srlEI3656er7EMubrq-mG9QqQ_aem_CNmn7xnfEgWIRe3NUFHtKQ/", "website":"https://www.mathrubhumi.com/"},
            {"paper":"jaihind", "linkin": "https://jaihindtv.in/", "website":"https://jaihindtv.in/"}
            ]

options = Options()
driver = webdriver.Edge()


time.sleep(10)  # Allow initial page load
go_through_diff_site(details)

driver.quit()
# for link in links:
    # print(link)
