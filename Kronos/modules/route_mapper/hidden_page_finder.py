from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

# Function to find hidden client-side pages using Selenium
def find_hidden_pages(driver, base_url, wordlist_file):
    try:
        # Load the wordlist of client-side routes
        with open(wordlist_file, "r") as file:
            routes = file.readlines()

        hidden_pages = []
        auth_required_pages = []  # List to track pages that require authorization

        # Step 1: Get the content of the home page (used as a baseline for comparison)
        driver.get(base_url)
        time.sleep(2)  # Wait for the home page to load

        try:
            # Example: Get the text of a unique element (such as a header or title)
            home_page_element = driver.find_element(By.TAG_NAME, "h1").text  # Example element: <h1>
        except NoSuchElementException:
            home_page_element = ""  # If no such element is found, set as empty

        # Step 2: Check each route and compare its content with the home page
        for route in routes:
            route = route.strip()  # Remove any trailing whitespace
            full_url = f"{base_url}/{route}"  # Directly append the route to the base URL

            try:
                # Navigate to the potential client-side route
                driver.get(full_url)
                time.sleep(2)  # Wait for the page to load (can adjust based on web app speed)

                # Check if a unique element exists and if it differs from the home page
                try:
                    route_page_element = driver.find_element(By.TAG_NAME, "h1").text  # Example element: <h1>
                    
                    # If the page differs from the home page, consider it a valid page
                    if route_page_element and route_page_element != home_page_element and full_url not in hidden_pages:
                        hidden_pages.append(full_url)
                    else:
                        # Check if this page requires authorization
                        if check_for_authorization(driver):
                            auth_required_pages.append(full_url)

                except NoSuchElementException:
                    pass  # If no unique element is found, skip this route

            except WebDriverException as e:
                print(f"Error navigating to {full_url}: {e}")

        return hidden_pages, auth_required_pages  # Return both discovered pages and auth-required pages

    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_file}' not found.")
        return [], []

# Enhanced function to check if the page requires authorization
def check_for_authorization(driver):
    try:
        # Check if the current URL contains signs of redirection to a login page (common pattern)
        current_url = driver.current_url.lower()
        if "login" in current_url or "auth" in current_url or "signin" in current_url:
            return True

        # Check for a login form by common IDs, names, or classes
        try:
            login_form = driver.find_element(By.ID, "login-form")  # Check for login form by ID
            if login_form:
                return True
        except NoSuchElementException:
            pass

        # Additional checks for other possible forms or login elements
        if "Login" in driver.page_source or "Unauthorized" in driver.page_source or "Sign In" in driver.page_source:
            return True
    except Exception as e:
        print(f"Error during authorization check: {e}")

    return False
