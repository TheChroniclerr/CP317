from price_finder import PriceManager, WebScraper
from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def main():
    # Setup driver
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(
        service=Service(GeckoDriverManager().install()),options=options)
    # Create scraper for each store
    stores = [WebScraper(driver,"Zehrs", "https://www.zehrs.ca/en"),
              WebScraper(driver, "No Frills", "https://www.nofrills.ca/en")
              ]
    queries = ["apples", "bananas", "milk"]
    manager = PriceManager()
    # Get items from each store
    for store in stores:
        store.open_site()
        results = store.scrape_list(queries)
        manager.add_products(results)
    
    driver.quit()

    best_items = manager.best_prices_for_list(queries)
    print(best_items)

if __name__ == "__main__":
    main()