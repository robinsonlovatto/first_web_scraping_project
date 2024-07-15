from browser.crawler.generic_crawler import GenericBrowserCrawler


store_to_scrap = "MercadoLivre"
keywords_to_search = "nintendo"

m1 = GenericBrowserCrawler(store_to_scrap).crawl(keywords_to_search)

store_to_scrap = "Amazon"
keywords_to_search = "playstation 5"

m2 = GenericBrowserCrawler(store_to_scrap).crawl(keywords_to_search)