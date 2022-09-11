import numpy as np
import pandas as pd
from pnp import pick_n_pay
from woolworths import woolworths
from shoprite import shoprite
from checkers import checkers


def main(user_basket, region, store):

    # empty dictionary to hold receipts for each store
    receipts = {}
    # empty list to hold the product details for each store
    pnp_df = []
    checkers_df = [] 
    shoprite_df = []
    woolworths_df = []

    for item in user_basket:

        if store.lower() == 'pnp':
            ### PNP ###
            pnp_dict = {} # product details found in pick n pay
            pnp_store = 'Pick n Pay' # set store name
            pnp_item, pnp_item_price, pnp_item_image = pick_n_pay(item, region) # extract product details
            # add product, its price and image url to store dictionary
            pnp_dict['product'] = pnp_item
            pnp_dict['price'] = pnp_item_price
            
            pnp_df.append(pnp_dict)

        if store.lower() == 'woolworths':
            ### WOOLWORTHS ###
            woolworths_dict = {} # product details found in woolworths
            woolworths_store = 'Woolworths' # set store name
            woolworths_item, woolworths_item_price, woolworths_item_image = woolworths(item, region) # extract product details
            # add product and its price to store dictionary
            woolworths_dict['product'] = woolworths_item
            woolworths_dict['price'] = woolworths_item_price
            
            woolworths_df.append(woolworths_dict)

        if store.lower() == 'checkers':
            CHECKERS_CARD = input('I have checkers card> ') # STREAMLIT ALTERNATIVE
            ### CHECKERS ###
            checkers_dict = {} # product details found in checkers
            checkers_store ='Checkers' # set store name
            checkers_available = checkers(item, region) # check availability of checkers store
            if checkers_available:
                checkers_item, checkers_item_price, checkers_item_image = checkers(item, region, checkers_card=CHECKERS_CARD) # extract product details
                # add product and its price to store dictionary
                checkers_dict['product'] = checkers_item
                checkers_dict['price'] = checkers_item_price
                
                checkers_df.append(checkers_dict)
            
            else: pass

        if store.lower() == 'shoprite':
            SHOPRITE_CARD = input('I have shoprite card> ') # STREAMLIT ALTERNATIVE
            ### SHOPRITE ###
            shoprite_dict = {} # product details found in shoprite
            shoprite_store = 'Shoprite'
            shoprite_available = shoprite(item, region)
            if shoprite_available:
                shoprite_item, shoprite_item_price, shoprite_item_image = shoprite(item, region, shoprite_card=SHOPRITE_CARD) # extract product details
                # add product and its price to store dictionary
                shoprite_dict['product'] = shoprite_item
                shoprite_dict['price'] = shoprite_item_price

                shoprite_df.append(shoprite_dict)
            
            else: pass
    
    # create a dataframe for each store in form of a receipt
    if store.lower() == 'pnp':
        ### PNP ###
        df_pnp = pd.DataFrame(pnp_df, columns=['product', 'price'])
        df_pnp = df_pnp.append({'product': 'TOTAL', 'price': df_pnp.price.sum()}, ignore_index=True).set_index('product')
        
        receipts['pnp'] = df_pnp

    if store.lower() == 'woolworths':
        ### WOOLWORTHS ###
        df_woolworths = pd.DataFrame(woolworths_df, columns=['product', 'price'])
        df_woolworths = df_woolworths.append({'product': 'TOTAL', 'price': df_woolworths.price.sum()}, ignore_index=True).set_index('product')
        
        receipts['woolworths'] = df_woolworths

    if store.lower() == 'checkers':
        if checkers_available:
            df_checkers = pd.DataFrame(checkers_df, columns=['product', 'price'])
            df_checkers = df_checkers.append({'product': 'TOTAL', 'price': df_checkers.price.sum()}, ignore_index=True).set_index('product')
            
            receipts['checkers'] = df_checkers
        else:
            pass

    if store.lower() == 'shoprite':       
        if shoprite_available:
            df_shoprite = pd.DataFrame(shoprite_df, columns=['product', 'price'])
            df_shoprite = df_shoprite.append({'product': 'TOTAL', 'price': df_shoprite.price.sum()}, ignore_index=True).set_index('product')

            receipts['shoprite'] = df_shoprite
        else:
            pass

    return receipts