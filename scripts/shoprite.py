from setregion import SetRegion
from scrapeproduct import ScrapeProducts
from process_item import ProcessItem
from memoizer import timed_lru_cache
from urls import SHOPRITE_SEARCH_URL, SHOPRITE_URL

def shoprite(item, region, checkers_card='n', shoprite_card='n'):

    available = False
    try:
        #region setter
        store = 'shoprite'
        region = SetRegion(SHOPRITE_URL, region)
        region_driver = region.shoprite_checkers_location()
        available =True
    except Exception:
        print('Shoprite is currently unavailable')  # STREAMLIT ALTERNATIVE
        available = False
        pass
    
    if available:
        #product scraping
        sp_shoprite = ScrapeProducts(item, SHOPRITE_URL, SHOPRITE_SEARCH_URL, store, region_driver)
        products = sp_shoprite.checkers_shoprite()

        #product processing
        pi = ProcessItem(products, checkers_card, shoprite_card, item, store)
        products, desired_products= pi.get_products()
        print(f"{item} found in {store}".upper().center(100, "#"))  # STREAMLIT ALTERNATIVE
        print(desired_products)                                     # STREAMLIT WRITE LIST ITEMS
        user_choice = input('choice > ')                            # STREAMLIT TEXT INPUT BOX
        product_details = pi.get_product_price(int(user_choice))

        region_driver.close()
        
        return product_details
    
    else:
        return None
