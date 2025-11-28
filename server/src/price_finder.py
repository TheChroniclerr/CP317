from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

class Product:
    def __init__(self, name, price_str,store):
        self.name = name
        self.price_str = price_str
        self.store = store          
        self.price_num, self.quantity_unit = self.normalize(price_str)

    def normalize(self,price_str):
        # Converts prices to universal unit so they can be easily compared
        # Extract product price 
        price = float(re.search(r"[\d\.]+", price_str).group())

        # Extract product unit
        unit_match = re.search(r"/([A-Za-z0-9]+)", price_str)
        if not unit_match:
            return price, "each"

        unit = unit_match.group(1).lower()

        # Convert all units to kg and get new price so they can be compared 
        if unit == "kg":
            return price, "kg"

        if unit == "g":
            return price * 1000, "kg"

        if unit == "100g":
            return price * 10, "kg"

        if unit == "lb":
            return price * 2.20462, "kg" 

        return price, unit

class WebScraper:
    def __init__(self,driver,store_name,url):
        self.driver = driver
        self.products = []
        self.store_name = store_name
        self.url = url

    def open_site(self):
        # Opens the site 
        self.driver.get(self.url)
        wait = WebDriverWait(self.driver, 115)

        # Closes the cookie banner if it appears
        try:
            cookie_button = wait.until(
            EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Close') or contains(., 'Got')]")
                )
            )
            cookie_button.click()

            # Wait to make sure the cookie button has disappeared 
            wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//button[contains(., 'Close') or contains(., 'Got')]")
                )
            )
        except:
            pass # no cookie banner appeared
        return
    def reset_page(self):
        # Resets page by returning to original url 
        wait = WebDriverWait(self.driver, 20)

        # Return to homepage to prevent search for next product to start before products have been scraped
        self.driver.get(self.url)

        # Wait for search bar to reappear
        wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@data-testid='autocomplete-input']"))
        )
        time.sleep(0.4)
    
    def search_products(self, query):
        # Searches for a singular item 
        wait = WebDriverWait(self.driver, 100)
        # Find the search bar, clear it and then search for the products
        search_bar = self.driver.find_element(By.XPATH, "//input[@data-testid='autocomplete-input']")
        search_bar.clear()
        search_bar.send_keys(query)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 300);")

        # Wait to make sure page has loaded 
        wait.until(EC.url_contains("search"))
        time.sleep(0.7)

        # Wait to make sure at least one product has appeared 
        try:
            wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[@data-testid='product-title']"))
            )
        except:
            time.sleep(1)
            return self.search_products(query)

        # Small wait for prices to appear 
        time.sleep(0.4)

        return

    def scrape_products_for(self, query):
        # Scrapes the products for a single query and returns list of results
        self.search_products(query)

        # Wait for products to appear 
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='product-title']")))
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[@data-testid='product-package-size']")))

        # Scrape the prices and names of the products 
        prices_el = self.driver.find_elements(By.XPATH, "//*[@data-testid='product-package-size']")
        names_el = self.driver.find_elements(By.XPATH,"//*[@data-testid='product-title']" )
        if len(prices_el) == 0 or len(names_el) == 0:
            return [] 

        max_items = 20
        limit = min(len(prices_el), len(names_el),max_items)

        results = [] 

        for i in range(limit):
            name = names_el[i].text.lower()
            price_str = prices_el[i].text

            if query.lower() not in name:
                continue  # Skip any items that don't have the query in their product name
            # Create product and add it to the list of products 
            product = Product(name, price_str, self.store_name)
            results.append(product)
            self.products.append(product)
        # If scrape did not work then recall the function 
        if len(results) == 0:
            time.sleep(1)
            return self.scrape_products_for(query)

        return results
    
    def scrape_list(self, queries):
        # Gets items for each query and adds it to the all_results dictionary
        all_results = {}
        for q in queries:
            result = self.scrape_products_for(q)
            all_results[q] = result
            self.reset_page()

        return all_results
    
class PriceManager:
    def __init__(self):
        self.all_products = []

    def add_products(self, products):
        # Adds the product to list 
        for product_list in products.values():
            for p in product_list:
                self.all_products.append(p)

    def best_price(self, item):
        # Finds the best price for a singular item 
        item = item.lower()
        matches = [p for p in self.all_products if item in p.name.lower()]
        if not matches:
            return None

        return min(matches, key=lambda p: p.price_num)
    
    def best_prices_for_list(self, queries):
        # Returns best price for all the items in a dictionary
        results = {}
        # Finds the best price for each item
        for q in queries:
            best = self.best_price(q)
            if best is None:
                results[q] = None
            else:
                # Stores the product in dictionary for easy printing on front-end
                results[q] = {
                    "name": best.name,
                    "store": best.store,
                    "price_num": best.price_num,
                    "price_str": best.price_str,
                    "unit": best.quantity_unit,
                }
        return results
