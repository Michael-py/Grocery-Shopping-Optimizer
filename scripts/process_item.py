import re

class ProcessItem:
    """
    Class to process all the data gotten from scraping process for an item
    
    Params:
        * products_dict - Dictionary containing details of all the products gotten from an item search
        * checkers_card - If the user has the checkers xtra savings card
        * shoprite_card - if the user has the shoprite xtra savings card
        * item - Product that is being processed 
        * store - Store that is being considered
        
    Functions:
        * match_product_url - Get all products that match only the item(product) of interest
        * get_item_price - Considering varying factors, set the appropriate price for an item or product
    """
    
    def __init__(self, products_dict, checkers_card, shoprite_card, item, store):
        """
        Class instance initializer
        """
        self.products = products_dict
        self.checkers_card = checkers_card
        self.shoprite_card = shoprite_card
        self.store = store
        self.item = item

    def match_product_url(self):
        """
        Function to find products in a list of products that match the item of interest
        
        Returns: A list of products that match the item of interest or all products
                if no match is found
        """
        # set pattern for item or product to match
        pattern = r'([\w+-/%?:\.]*' + str(self.item.replace(' ', '\-')) + '[\w+-/%?]*)'
        # list to hold all products that match set pattern
        wanted_products = []
        # list to hold products if no match is found
        all_products = []
        # iterate through products
        for product in self.products:
            # check for a match
            match = re.match(pattern, product['Url'].lower())

            if match:
                # append product to list of products that match pattern
                wanted_products.append(product)

            else:
                # append product to list of products that do not match pattern
                all_products.append(product)
        # return products that do not match pattern if the length
        # of the list of products that match the pattern is 0
        return all_products if len(wanted_products) == 0 else wanted_products
    
    def get_products(self):

        # call match_product_url function
        products = self.match_product_url()
        # create a dictionary of products in form of a menu
        desired_products = [{y: (x['Name'], x['Price'], x['Image'])} for y, x in enumerate(products, start=1)]
        sorted_desired_products = sorted(desired_products, key=lambda x: list(x.values())[0][1])
        # print menu
        return products, sorted_desired_products


    def get_product_price(self, user_choice):
        
        # get list of products and sorted desired products
        products, sorted_desired_products = self.get_products()

        # empty string to hold user's desired product
        product_name = ''

        # iterate through item-matched products menu
        for product in sorted_desired_products:
            # iterate through the product in the menu
            for idx, name in product.items():
                # compare user choice to product in menu
                # if product in menu, set empty string to product name
                if idx == user_choice:
                    product_name += name[0]
        # iterate through products list (products details)
        for product in products:
            # if the product name matches the product selected by the user
            if product['Name'] == product_name:
                # check for conditions about the store (checkers), the user and the promo type (with xtra savings card or not)
                if self.store == "checkers" and re.match(r'with card', product['Name']) and self.checkers_card.lower() == 'y':
                    # set price accordingly
                    price = product['Promo price'] if product['Promo price'] and product['Promo price'] < product['Price'] else product['Price']
                # check for conditions about the store (shoprite), the user and the promo type (with xtra savings card or not)
                elif self.store == "shoprite" and re.match(r'with card', product['Name']) and self.shoprite_card.lower() == 'y':
                    # set price accordingly
                    price = product['Promo price'] if product['Promo price'] and product['Promo price'] < product['Price'] else product['Price']
                # if stores not shoprite nor checkers
                else:
                    # set price accordingly
                    price = product['Promo price'] if product['Promo price'] and product['Promo price'] < product['Price'] else product['Price']
                # return product name and price
                return (product['Name'], price, product['Image']) if product['Name'] and price else ('Unknown', 0)