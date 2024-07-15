from datetime import datetime
import json
import time

from bs4 import BeautifulSoup
import pandas as pd
from browser.crawler.default_crawler import AbstractCrawler
from browser.actions.browser_actions import action_dict

class GenericBrowserCrawler(AbstractCrawler):
    def __init__(self, store_config_key):
        super().__init__()
        self.type = store_config_key
        self.steps = json.loads(self.get_steps(self.type))
        if self.steps is None:
            raise("Config not found!")
        

    def crawl(self, query):
        self.query = query
        self.execute_before()
        df = self.execute_main()
        self.execute_after()
        self.save_data(df)

    def execute_main(self):
        self.browser.get(f"{self.steps["link"]["path"]}{self.query.replace(' ', self.steps["link"]["connector"])}")
        time.sleep(5)
        self.content = self.extraction()
        return self.transform_df(self.content)

    def execute_before(self):
        before = self.steps["script"]["before"]
        if before:
            for action in before:
                if action_dict[action] is None:
                    raise("Action does not exist!")
                action_dict[action](self.browser, before[action])
            return

    def execute_after(self):
        after = self.steps["script"]["after"]
        if after:
            for action in after:
                if action_dict[action] is None:
                    raise("Action does not exist!")
                action_dict[action](self.browser, after[action])
            return
    
    def extraction(self):
        self.html = self.browser.page_source

        soup = BeautifulSoup(self.html, "html.parser")

        if self.steps["search"]["custom"]:
            results = soup.find_all(self.steps["search"]["tag"], self.steps["search"]["custom"])
        else:
            results = soup.find_all(self.steps["search"]["tag"], class_ = self.steps["search"]["class"])

        data = []

        for result in results:
            product = {}
            for step in self.steps["product"]:
                value = self.steps["product"][step]
                try:
                    content = eval(value)
                except:
                    content = None

                product[step] = content
            data.append(product)
        self.browser.close()
        return data

    def transform_df(self, data):
        df = pd.DataFrame(data)
        df = df.assign(keyword = self.query)
        df = df.assign(dateTimeReference = datetime.now().isoformat())
        df = df.assign(crawlerType = "Browser")
        return df