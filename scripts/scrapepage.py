import time
from memoizer import timed_lru_cache
from bs4 import BeautifulSoup as soup

class ScrapePage:
    """
    Class to scrape the web page of interested stores
    
    Params:
        * item - Grocery product of interest
        * store_url - Interested store's base url
        * store_search_url - Interested store's search url
        * driver - Driver object perculiar to store of interest
    
    Functions:
        * store_page() - Searches for a product and returns a souped search result
        
    """
    
    def __init__(self, item, store_url, store_search_url, driver):
        """
        Class instance initializer
        """
        self.item = item
        self.store_url = store_url
        self.store_search_url = store_search_url
        self.driver = driver
        
    @timed_lru_cache()
    def store_page(self):
        """
        Search store of interest for item of interest
        
        Returns: A beautiful soup parsed object
        """
        try:
            # get web page of search result
            self.driver.get(self.store_search_url+self.item+'&Dy=1')
        except Exception:
            # wait for full page load
            print('waiting for full page load')
        time.sleep(10) # pause
        # using beautiful soup, parse the page source from gotten web page
        page_soup = soup(self.driver.page_source, 'html.parser')
        # return beautiful soup parsed object
        return page_soup    
    