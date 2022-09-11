import re
from bs4 import BeautifulSoup as soup
from urls import PNP_SEARCH_URL, PNP_URL, WOOLWORTHS_SEARCH_URL, WOOLWORTHS_URL,\
                CHECKERS_SEARCH_URL, CHECKERS_URL, SHOPRITE_SEARCH_URL, SHOPRITE_URL
from scrapepage import ScrapePage
from memoizer import timed_lru_cache

class ScrapeProducts:
    """
    Class to extract grocery products details from the souped html
    
    Params:
        * item - Product of interest
        * store_url - Base url of store of interest
        * store_search_url - Search url of store of interest
        * store - Store of interest
        * driver - Perculiar driver of the store of interest
        
    Functions:
        * page() - Creates `ScrapePage` instance
        * pick_n_pay() - Extracts products from pick_n_pay souped search results
        * checkers_shoprite() - Extracts products from checkers and shoprite souped search results
        * woolworths() - Extracts products from woolworths souped search results
    """
    
    def __init__(self, item, store_url, store_search_url, store, driver):
        """
        Class instance initializer
        """
        self.item = item
        self.store_url = store_url
        self.store_search_url = store_search_url
        self.store = store
        self.driver = driver
    
    @timed_lru_cache()
    def page(self):
        """
        Creates a ScrapePage instance
        """
        # create ScrapePage instance
        page = ScrapePage(self.item, self.store_url, self.store_search_url, self.driver)
        # return ScrapePage instance
        return page
    @timed_lru_cache()
    def pick_n_pay(self):
        """
        Function to extract all the product brands on a souped search page html for product of interest
        
        Returns: A list of dictionaries containing product details from pick n' pay
        """
        # call page function
        page = self.page()
        # get souped search page html
        page_soup = page.store_page()
        # locate the containers holding the products and their details
        products_container = page_soup.find_all('div', class_='product-card-grid')
        # empty list to hold dictionary of product details
        products = []
        # iterate through all the product containers found
        for product in products_container:
            # empty dictionary to hold details of each product
            product_dict = {}
            # locate and extract the name of the product
            name = product.find('div', class_='item-name').get_text()
            # locate and extract the price of the product
            # strip all white spaces(newlines, tabs, spaces) and currency symbol 'R'
            try:
                price = product.find('div', class_='product-price').find('div', class_='item-price')\
                                .find('div', class_='currentPrice').get_text()\
                                .strip('\n').strip('\t').lstrip('R').strip().lstrip('R')
            except Exception:
                price = product.find('div', class_='product-price').find('span', class_='priceDiv')\
                                .find('div', class_='normalPrice').get_text()\
                                .strip('\n').strip('\t').lstrip('R').strip().lstrip('R')
                
            # pick n pay prices are not separated by decimal('.')
            # decimal will be added
            l_price = list(price)
            l_price.insert(-2, '.')
            # locate and extract product link
            url = product.find('a')['href']
            # locate and extract product image
            image = product.find('img')['src']
            # locate and extract product promo
            promo = product.find('div', id='promotionContainer').get_text().strip('\t').strip('\n').strip()
            
            try:
                # extract promo price if any
                promo_price = float(re.search(r'\d+[\.]?\d+', promo_price).group())
            
            except Exception:
                # set promo price to None if not found
                promo_price = None
            # locate and extract minimum and maximum orders 
            min_max_purchase = product.find('div', class_='minMaxQuantityMsgContainer')\
                                .get_text().strip('\n').strip()  
            # build product details
            product_dict['Name'] = name # add name to dictionary
            product_dict['Price'] = float(''.join(l_price)) # add price to dictionary
            product_dict['Promo'] = promo if promo else None # add promo to dictionary
            product_dict['Promo price'] = promo_price # add promo price to dictionary
            product_dict['Min_Max'] = min_max_purchase if min_max_purchase else None # add min max purchase order
            product_dict['Url'] = self.store_url + url # add products url to dictionary
            product_dict['Image'] = image # add product's image link to dictionary
            # append product details to list of products
            products.append(product_dict)
        # return product details
        return products
    @timed_lru_cache()
    def checkers_shoprite(self):
        """
        Function to extract all the product brands on a souped search page html for product of interest
        
        Returns: A list of dictionaries containing product details from checkers and shoprite
        """
        # call page function
        page = self.page()
        # get souped search page html
        page_soup = page.store_page()
        # locate container holding products and their details
        item_div = page_soup.find_all('div', class_='item-product')
        # empty list to hold dictionaries of products details
        products = []
        # iterate through every item in the list of items
        for item in item_div:
            # empty dictionary to hold product details
            product_dict = {}
            # locate and extract the product name
            name = item.find('h3', class_='item-product__name').get_text().strip()
            # locate and extract the product price
            price = item.find('div', class_='special-price__price').get_text().strip().lstrip('R')
            # locate and extract the product url
            url = item.find('div', class_='item-product__image').find('a')['href']
            # locate and extract the product image
            image = item.find('div', class_='item-product__image').find('a').find('img')['src']
            
            try:
                # if product is on promo, locate and extract promo details and
                # extract promo price
                promo = item.find('div', class_='special-price__extra__price').find('span', class_='now').get_text().strip()
                promo_price = float(re.search(r'\d+[\.]\d+', promo)).group()
            except Exception:
                # if no promo found, set promo and promo price to None
                promo = None
                promo_price = None
            
            try:
                # check for promo validity
                validity = item.find('span', class_='item-product__valid').get_text().strip('\n').strip()
            except Exception:
                # set validity to None if no validity found
                validity = None
            # build product details
            product_dict['Name'] = name # add product name to dictionary
            product_dict['Price'] = float(re.search(r'\d+\.\d+', price).group()) # add product price to dictionary
            product_dict['Promo'] = promo # add promo details to dictionary
            product_dict['Promo price'] = promo_price # add promo price to dictionary
            product_dict['Validity'] = validity # add promo validity to dictionary
            product_dict['Url'] = self.store_url+url # add product url to dictionary
            product_dict['Image'] = self.store_url+image # add product image to dictionary
            # append product details to list of products
            products.append(product_dict)
        # return products details 
        return products
    @timed_lru_cache()
    def woolworths(self):
        """
        Function to extract all the product brands on a souped search page html for product of interest
        
        Returns: A list of dictionaries containing product details from woolworths
        """
        # call page function
        page = self.page()
        # get souped search page html
        page_soup = page.store_page()
        # locate container holding products and their details
        products_container = page_soup.find_all('div', class_='product-list__item')
        # empty list to hold dictionaries of products details
        products = []
        # iterate through every item in the list of items
        for product in products_container:
            # empty dictionary to hold product details
            product_dict = {}
            
            try:
                # locate and extract the product name
                name = product.find('div', class_='product-card__name').get_text().strip('\n').strip('\t').strip()
            except Exception:
                # set to unknown if no product name
                name = "Unknown"
            try:
                # locate and extract the product price
                price = product.find('strong', class_='price').get_text().strip('\n').strip('\t').strip().lstrip('R')
            except Exception:
                # set to None if no price found
                price = None

            try:
                # locate and extract price before promo
                promo_original_price = eval(product.find('strong', class_='price--strikethrough price--original')\
                                            .get_text().strip('\n').strip('\t').strip().lstrip('R'))
            except Exception:
                # if no promo, set to None
                promo_original_price = None
            # set promo price to None
            promo_price = None
            # check if price before promo exists
            if promo_original_price:
                # set promo price to the previously extracted price
                # because on the website, if there's a promo, the 
                # promo price is put in the same position where
                # the regular price should be
                promo_price = price
                # set price to be original price that has been moved
                # to a different position
                price = promo_original_price
                
            try:
                # locate and extract the product image
                image = product.find('div', class_='product--image').find('img')['src']
            except Exception:
                # set to None if not found
                image = None
            # locate and extract the product url
            url = self.store_url+product.find('a', href=True)['href']
            # build product details
            name_wt = name.rfind(' ')
            product_dict['Name'] = name[:name_wt] + name[name_wt+1:] # add product name to dictionary
            product_dict['Price'] = float(price) if price else 0# add product price to dictionary
            product_dict['Promo price'] = promo_price # add promo price to dictionary
            product_dict['Url'] = url # add product url to dictionary
            product_dict['Image'] = image # add product image to dictionary
            # append product details to products list
            products.append(product_dict)
        # return list of products
        return products
        