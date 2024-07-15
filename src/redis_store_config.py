from browser.tools.redis import RedisClient

redis = RedisClient.get()
mercado_livre_config = """{
    "link": {
        "path": "https://lista.mercadolivre.com.br/",
        "connector": "-"
    },
    "script": {
        "before": {},
        "after": {}
    },
    "search": {
        "tag": "div",
        "class": "ui-search-result",
        "custom": ""
    },
    "product": {
        "title": "result.find(\\"h2\\", class_=\\"ui-search-item__title\\").text.strip()",
        "price": "result.find(\\"span\\", class_=\\"andes-money-amount__fraction\\").text.strip()",
        "link_tag": "result.find(\\"a\\", class_=\\"ui-search-link\\").get(\\"href\\")"
    }
}"""

redis.set("MercadoLivre", mercado_livre_config)

amazon_config = """{
    "link": {
        "path": "https://www.amazon.com.br/s?k=",
        "connector": "+"
    },
    "script": {
        "before": {
            "goto": "https://www.amazon.com.br"
        },
        "after": {}
    },
    "search": {
        "tag": "div",
        "class": "",
        "custom": {
            "data-component-type": "s-search-result"
        }
    },
    "product": {
        "title": "result.find('span',{'class': 'a-size-base-plus a-color-base a-text-normal'}).text.strip()",
        "price": "result.find('span',{'class': 'a-price-whole'}).text.strip()",
        "link_tag": "result.find('a',{'class': 'a-link-normal s-no-outline'}).get(\\"href\\")"
    }
}
"""

redis.set("Amazon", amazon_config)
