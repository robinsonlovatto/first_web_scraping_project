import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

class RequestML:

    def execute_command(self, query):
        url = f"https://lista.mercadolivre.com.br/{query.replace(' ','-')}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")

            results = soup.find_all("div", class_="ui-search-result")
            data = []

            for result in results:
                link = None
                title = result.find("h2", class_="ui-search-item__title").text.strip()

                price = result.find("span", class_="andes-money-amount__fraction").text.strip()
                link_tag = result.find("a", class_="ui-search-link")
                if link_tag:
                    link = link_tag.get("href")
                
                data.append({"Product": title, "Price": price, "URL": link})
                
        return data

    def transform_df(self, query):
        data = self.execute_command(query)
        df = pd.DataFrame(data)
        
        return df    
     
crawler = RequestML()
dataframe = crawler.transform_df("Nintendo")

print(dataframe)    