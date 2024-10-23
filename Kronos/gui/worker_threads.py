# worker_threads.py
from PySide6.QtCore import QThread, Signal
from modules.route_mapper.crawler import start_crawler
from modules.route_mapper.hidden_page_finder import find_hidden_pages
from selenium import webdriver
import re

class CrawlerWorker(QThread):
    crawler_finished = Signal(list)

    def __init__(self, input_value):
        super().__init__()
        self.input_value = input_value  # Can be either a full URL or a port

    def is_valid_url(self, url):
        # Regex to check if the input is a valid URL (starts with http:// or https://)
        url_regex = re.compile(r'^(http|https)://')
        return re.match(url_regex, url)

    def run(self):
        try:
            if self.is_valid_url(self.input_value):
                url = self.input_value  # Use the input directly as a URL if valid
            else:
                url = f"http://localhost:{self.input_value}"  # Construct a URL using localhost and the port
            
            # Start the crawling process with the constructed or provided URL
            pages = start_crawler(url)
            self.crawler_finished.emit(pages)
        except Exception as e:
            self.crawler_finished.emit([f"An error occurred: {e}"])

class HiddenPageWorker(QThread):
    hidden_pages_found = Signal(list, list)

    def __init__(self, base_url, wordlist_file):
        super().__init__()
        self.base_url = base_url
        self.wordlist_file = wordlist_file

    def run(self):
        driver = webdriver.Firefox()
        try:
            hidden_pages, auth_required_pages = find_hidden_pages(driver, self.base_url, self.wordlist_file)
            self.hidden_pages_found.emit(hidden_pages, auth_required_pages)
        finally:
            driver.quit()
