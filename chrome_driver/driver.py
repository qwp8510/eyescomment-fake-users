from os import path
from bs4 import BeautifulSoup
from selenium import webdriver

CURRENT_PATH = path.dirname(path.abspath(__file__))


class ChromeDriver():
    chrome_driver_dir = 'chromedriver'

    def __init__(self):
        self._browser = None

    @property
    def browser(self):
        if not self._browser:
            self._browser = webdriver.Chrome(
                executable_path=(path.join(CURRENT_PATH, self.chrome_driver_dir)))
        return self._browser

    @property
    def page_source(self):
        return BeautifulSoup(self.browser.page_source, 'html.parser')

    def close(self):
        self.browser.close()
