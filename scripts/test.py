from main import main

REGION = 'cape town'                            # STREAMLIT ALTERNATIVE - SET DEFAULT TO 'cape town'
USER_BASKET = ['chicken']                       # STREAMLIT ALTERNATIVE   
STORES = ['pnp', 'woolworths']                  # STREAMLIT ALTERNATIVE 

STORES_RECEIPTS = []
STORES_TOTALS = {}

for store in STORES:
    receipts = main(USER_BASKET, REGION, store)
    STORES_RECEIPTS.append(receipts)


for receipts in STORES_RECEIPTS:
    for store, receipt in receipts.items():
        STORES_TOTALS[store] = receipt.loc['TOTAL'][0]
        print(f"{store} receipt")                       # STREAMLIT ALTERNATIVE
        print(receipt)                                  # STREAMLIT ALTERNATIVE

### MAKE RECOMMENDATION
try:
    # get least total basket amount
    min_total = min(STORES_TOTALS.values())
    # iterate throough dictionary of stores totals
    for store, total in STORES_TOTALS.items():
        # get the store with the least total basket amount
        if total == min_total:
            print()
            print()
            # make recommendation
            print(f" we recommend shopping from: {store} ".upper().center(50, "*")) # STREAMLIT ALTERNATIVE

except:
    print('No item found')