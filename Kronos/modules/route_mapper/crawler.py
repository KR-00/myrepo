# modules/route_mapper/crawler.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import re

def is_unique_page(driver, unique_pages, url):
    time.sleep(2)
    try:
        page_content = driver.find_element(By.TAG_NAME, 'body').text
        if page_content not in unique_pages:
            unique_pages[page_content] = url
            return True
    except NoSuchElementException:
        pass
    return False

def discover_pages(driver, base_url):
    pages_to_check = [base_url]
    unique_pages = {}
    discovered_urls = []
    while pages_to_check:
        current_url = pages_to_check.pop(0)
        if '/redirect' in current_url:
            continue
        if re.search(r'legal\.md$', current_url):
            continue
        try:
            driver.get(current_url)
            if not current_url.startswith(base_url):
                continue
            if re.search(r'\.(pdf|md|jpg|png|zip|gif|jpeg|exe|doc|docx|txt)$', current_url):
                continue
            if is_unique_page(driver, unique_pages, current_url):
                discovered_urls.append(current_url)
                links = driver.find_elements(By.TAG_NAME, "a")
                for link in links:
                    href = link.get_attribute("href")
                    if href and href.startswith(base_url) and href not in discovered_urls and href not in pages_to_check:
                        pages_to_check.append(href)
        except WebDriverException as e:
            continue
    return discovered_urls

def start_crawler(input_value):
    # Check if the input is a full URL or a port number
    if input_value.startswith("http://") or input_value.startswith("https://"):
        base_url = input_value  # Full URL is provided
    else:
        base_url = f"http://localhost:{input_value}"  # Assume it's a port and build the URL

    driver = webdriver.Firefox()
    discovered_pages = []
    try:
        driver.get(base_url)
        discovered_pages = discover_pages(driver, base_url)
    except Exception as e:
        discovered_pages = [f"An error occurred: {e}"]
    finally:
        driver.quit()
    
    return discovered_pages  # Return only discovered pages
