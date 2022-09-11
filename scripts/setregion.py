# library for time manipulation
import time
# library to generate random figures
import random
# Libraries for web brower automation and web scraping
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SetRegion:
    """
    Class to set the region on each website, where possible, to
    the region of interest for all the stores of interest
    
    Params:
        * store : Url of store of interest
        
    Functions:
        * get_store() - Initial configuring and opening up store's base url
        * pick_n_pay_location() - Changes location and gets a perculiar driver for pick n' pay
        * shoprite_checkers_location() - Changes location and get a perculiar driver for shoprite and checkers
        * woolworths() - Gets driver for woolworths
    """
    
    def __init__(self, store, region):
        """
        Class instance initializer
        """
        self.store = store
        self.region = region
        
    def get_store(self):
        """
        Opens up the Chrome Browser goes to the url specified in the class instantiation, 
        with several parameters to disable website objects that can potentially 
        slow down the page load such as; images, extensions and infobars.
        
        Javascript which can also lead to slow page load can not be disabled 
        because many operations that are intended to be done with selenium
        are heavily dependent on the Javascript for the website to be enabled.
        
        Params: None
        
        Returns: A driver object perculiar to a store's url
        """
        
        chrome_options = webdriver.ChromeOptions() # create chrome_options object
        prefs = {"profile.managed_default_content_settings.images": 2} # disable images
        chrome_options.add_experimental_option("prefs", prefs) # set disable images object
        chrome_options.add_argument("--disable-extensions") # disable extensions
        chrome_options.add_argument("disable-infobars") # disable infobars
        options = Options()  # create an options object
        options.headless = False # allow user interface pop up
        options.add_argument('user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 \
                            (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"') # set user agents
        driver = webdriver.Chrome(options=options, chrome_options=chrome_options) # create driver object with options and chrome_options
        driver.implicitly_wait(5) # make driver wait implicitly for set time
        time.sleep(3) # pause execution for 3 secs
        
        try:
            driver.get(self.store) # get store web page

        except Exception:
            print('waiting for full page load...') # wait for full page load
        time.sleep(10) # pause
        # return driver object
        return driver
    
    def pick_n_pay_location(self):
        """
        Changes the default location for pick n' pay store to a store 
        in the preferred region 
        
        Params: None
        
        Returns: A driver object perculiar to pick n' pay
        """
        driver = self.get_store() # get pick n' pay web page
        # locate the initial modal class to accept or reject cookies
        custom_modal = driver.find_element(By.CLASS_NAME, 'modal-footer')
        # locate the first button of the modal class
        close_button = custom_modal.find_element(By.TAG_NAME, 'button')
        time.sleep(5) # pause 
        # click on the button to clear the modal
        close_button.send_keys(Keys.RETURN)
        # locate the region selector
        button_loc = driver.find_element(By.CLASS_NAME, 'js-region-base-store-display-area')
        button = button_loc.find_element(By.TAG_NAME, 'a')
        time.sleep(1) # pause
        button.click() # click the region selector button
        # get the last region "west cape"
        region_button = driver.find_elements(By.CLASS_NAME, 'js-region-key')[-1]
        time.sleep(2) # pause
        # click on the selected region
        region_button.click()
        # get the first region in 'west cape' - the selected region
        wanted_store_button = driver.find_elements(By.CSS_SELECTOR, 'div[data-region-key="Western Cape"]')[0]\
                                .find_element(By.TAG_NAME, 'p')
        time.sleep(2) # pause
        # click on the first region in 'west cape'
        wanted_store_button.click()
        time.sleep(3) # pause
        
        # return driver object
        return driver
    
    def shoprite_checkers_location(self):
        """
        Changes the default location for shoprite and checkers stores to a store 
        in the preferred region and a store that is the closest to the 
        user's current position.
        
        Params: None
        
        Returns: A driver object perculiar to shoprite or checkers
        """
        driver = self.get_store() # get checkers or shoprite web page
        # locate region selector button
        store_button = driver.find_element(By.CLASS_NAME, 'header__your-store')
        time.sleep(3) # pause
        # click store selection button
        store_button.click()
        # locate input box for searching for regions
        input_box = store_button.find_element(By.ID, 'storeFinderInput')
        # clear the input box 
        input_box.clear()
        time.sleep(2) # pause
        # iterate through characters in the preferred region
        for char in self.region:
            # input characters one after the other into the input box
            input_box.send_keys(char)
            # pause at random times between .1sec and .5secs
            time.sleep(round(random.uniform(.1, .5),2))
        # hit enter to search for region inputted
        input_box.send_keys(Keys.ENTER)
        time.sleep(2) # pause
        # get all stores found in the region
        stores = driver.find_elements(By.CLASS_NAME, 'nav-store-your-results')
        time.sleep(3) # pause
        # empty list to hold stores and their distance relative to the user
        stores_list = []
        # iterate through the stores (web elements) found
        for store in stores:
            # extract the name from the store web element
            store_name = store.find_element(By.TAG_NAME, 'a').get_attribute('innerHTML').strip()
            time.sleep(1) # pause
            # extract the distance from the store web element
            store_distance = store.find_element(By.CLASS_NAME, 'store-distance')\
                            .find_element(By.TAG_NAME, 'span').get_attribute('innerHTML').strip()
            # append the store name and the store distance to the empty list created prior
            stores_list.append((store_name, store_distance))
        # sort the stores list by their distance in ascending order
        stores_list.sort(reverse=True, key=lambda x: x[1])
        # extract the nearest store - store with minimum distance
        nearest_store = stores_list[-1][0]
        # clear input box
        input_box.clear()
        time.sleep(2)# pause
        # iterate through the characters of the nearest store
        for char in nearest_store:
            # send each character to the input box
            input_box.send_keys(char)
            # pause at random times
            time.sleep(round(random.uniform(.1, .5),2))
        # hit enter to search for inputed store
        input_box.send_keys(Keys.ENTER)
        time.sleep(2) # pause
        # get the first store to appear
        store_wanted = driver.find_element(By.CLASS_NAME, 'nav-store-your-results')
        time.sleep(2) # pause
        # locate container containing the button to set store as default
        select_store_button_container = store_wanted.find_element(By.CLASS_NAME, 'sl-container')
        time.sleep(2) # pause
        # select button to set store as default
        button = select_store_button_container.find_element(By.TAG_NAME, 'button')
        time.sleep(3) # pause
        # click button to set store as default
        button.click()
        time.sleep(1) # pause
        # return driver perculiar to shoprite and checkers
        return driver
    
    def woolworths(self):
        """
        Function to get the perculiar web driver for woolworths.
        Woolworths has no option for region selection.
        """
        driver = self.get_store() # get woolworths web page
        # return woolworths peculiar driver
        return driver