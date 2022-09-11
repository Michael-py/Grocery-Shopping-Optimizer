from setregion import SetRegion
from scrapeproduct import ScrapeProducts
from process_item import ProcessItem
from memoizer import timed_lru_cache
from urls import PNP_SEARCH_URL, PNP_URL

def pick_n_pay(item, region, checkers_card='n', shoprite_card='n'):

    #region setter
    store = 'pick n pay'
    region = SetRegion(PNP_URL, region)
    region_driver = region.pick_n_pay_location()

    #product scraping
    sp_pnp = ScrapeProducts(item, PNP_URL, PNP_SEARCH_URL, store, region_driver)
    products = sp_pnp.pick_n_pay()

    #product processing
    pi = ProcessItem(products, checkers_card, shoprite_card, item, store)
    products, desired_products= pi.get_products()
    print(f"{item} found in {store}".upper().center(100, "#"))  # STREAMLIT ALTERNATIVE
    print(desired_products)                                     # STREAMLIT WRITE LIST ITEMS
    user_choice = input('choice > ')                            # STREAMLIT TEXT INPUT BOX
    product_details = pi.get_product_price(int(user_choice))

    region_driver.close()
    
    return product_details