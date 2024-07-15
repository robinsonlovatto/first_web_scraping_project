import os
from selenium import webdriver
from dotenv import load_dotenv
from pathlib import Path

class GenericBrowser:

    def __init__(self):
        dotenv_path = Path.cwd() / '.env'
        load_dotenv(dotenv_path=dotenv_path)
    
        self.browser = None
        self.options = webdriver.ChromeOptions()

        self.default_options = [
            "--no-sandbox",
            "--disable-gpu",
            "--disable-setuid-sandbox",
            "--disable-web-security",
            "--disable-dev-shm-usage",
            "--memory-pressure-off",
            "--ignore-certificate-errors",
            "--disable-features=site-per-process"
            ]

    def get_browser(self, args: list[str] = None):
        new_args = args
        if args is None:
            new_args = self.default_options
        self.set_options(new_args)
        return webdriver.Chrome(options=self.options)

    def is_headless(self):
        headless = os.getenv('HEADLESS')
        if headless is None or headless=="True":
            self.options.add_argument("--headless")

    def set_options(self, args: list[str] | None):
        self.is_headless()
        self.set_proxy()
        if args:
            for arg in args:
                self.options.add_argument(arg)

    def set_proxy(self):
        if os.getenv("USE_PROXY"):
            user = os.getenv("PROXY_USER")
            password = os.getenv("PROXY_PASSWORD")
            url = os.getenv("PROXY_URL")
            port = os.getenv("PROXY_PORT")
            proxy_provider = f'http://{user}:{password}@{url}:{port}'
            self.options.add_argument(f'--proxy-server={proxy_provider}')

    def close(self):
        return self.browser.quit()