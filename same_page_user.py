from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from os import path
import time
import logging


logger = logging.getLogger(__name__)
CURRENT_PATH = path.dirname(path.abspath(__file__))
BASE_URL = 'http://localhost:8000/'


class ChromeDriver():
    chrome_driver_dir = 'chromedriver_86\chromedriver'

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


class PageOperators(ChromeDriver):
    def __init__(self, delay=1):
        self.delay = delay
        super().__init__()

    def click(self, link_text):
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.LINK_TEXT, link_text)))
            result = self.browser.find_element_by_link_text(link_text)
            result.click()
        except TimeoutException:
            logger.error(
                'loading page over-time: {}, so fail finding element link text {}'.format(self.delay, link_text))

    def get_page_source_until_class_loading(self, class_name):
        try:
            myElem = WebDriverWait(self.browser, self.delay).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return self.page_source
        except TimeoutException:
            logger.error(
                'loading page over-time: {}, so fail finding element class {}'.format(self.delay, class_name))

    def set_delay(self, delay):
        self.delay = delay

    def load_browser_url(self, url):
        self.browser.get(url)


# def get_href(divs):
#     for element in divs:
#         return element.find('a')['href']

def _get_comments(comments_object):
    for comment_object in comments_object:
        yield comment_object.text

def click_channel_into_videos_page(operators, channel):
    operators.click(channel)


def click_video_into_video_detail_page(operators, video):
    operators.click(video)


def _valid_get_comment(comments):
    return len(comments) > 0

def run():
    channel_name = 'Onion Man'
    video_name = 'Onion Man | 叛徒'
    page_operators = PageOperators()
    target_url = BASE_URL + 'eyescomment'
    page_operators.load_browser_url(target_url)
    click_channel_into_videos_page(page_operators, channel_name)
    click_video_into_video_detail_page(page_operators, video_name)
    page_source = page_operators.get_page_source_until_class_loading('comment')
    comments = list(_get_comments(page_source.find_all('div', {'class': 'text'})))
    if _valid_get_comment(comments):
        logger.info('testing get channel {} video {} comments succeed'.format(
            channel_name, video_name))
    else:
        logger.error('testing get channel {} video {} comments fail'.format(
            channel_name, video_name))
    page_operators.close()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)-15s:%(levelname)s:%(name)s:%(message)s')
    run()
