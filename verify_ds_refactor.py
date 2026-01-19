from aliexpress_api.api import AliexpressApi, models
import traceback

# Using same credentials as test_ds_api.py
KEY = "518448"
SECRET = "o1bnfYAOvpIBqLJyU1HIaTJGww76sCBo"
TOKEN = ""

api = AliexpressApi(
    key=KEY,
    secret=SECRET,
    language=models.Language.EN,
    currency=models.Currency.USD,
    token=TOKEN,
)

def test_get_ds_categories():
    print("\n--- Testing get_ds_categories ---")
    try:
        response = api.get_ds_categories(language="en")
        print("Successfully retrieved categories.")
        
        # Verify it's a DsCategoryGetResponse
        if isinstance(response, models.DsCategoryGetResponse):
            print(f"Response is typed: {type(response).__name__}")
            print(f"Found {len(response.categories)} categories.")
            if response.categories:
                cat = response.categories[0]
                print(f"First category: {cat.category_name} (ID: {cat.category_id})")
        else:
            print(f"Response is NOT typed as expected. Type: {type(response)}")

    except Exception as e:
        print(f"Error in get_ds_categories: {e}")
        traceback.print_exc()

def test_text_search_ds():
    print("\n--- Testing text_search_ds with Product ID ---")
    # Using Product ID as keyword
    keywords = "1005010479059762" 
    try:
        response = api.text_search_ds(keywords=keywords, country="FR", page_size=1)
        print("Successfully retrieved search response.")
        
        if isinstance(response, models.DsTextSearchResponse):
            print(f"Response is typed: {type(response).__name__}")
            if response.products:
                product = response.products[0]
                print(f"Found product: {product.title} (ID: {product.itemId})")
                print(f"Price: {product.salePrice} {product.salePriceCurrency}")
            else:
                print("No products in search result.")
        else:
            print(f"Response is NOT typed as expected. Type: {type(response)}")

    except Exception as e:
        print(f"Error in text_search_ds: {e}")
        # traceback.print_exc()

def test_get_ds_product():
    print("\n--- Testing get_ds_product ---")
    product_id = "1005010479059762"
    try:
        response = api.get_ds_product(product_id=product_id, ship_to_country="FR")
        print("Successfully retrieved product details.")
        
        if isinstance(response, models.DsProductGetResponse):
            print(f"Response is typed: {type(response).__name__}")
            if response.ae_item_base_info_dto:
                print(f"Product Title: {response.ae_item_base_info_dto.subject}")
            
            if response.ae_item_sku_info_dtos:
                sku = response.ae_item_sku_info_dtos[0]
                print(f"First SKU ID: {sku.sku_id} - Price: {sku.sku_price} {sku.currency_code}")
                return sku.sku_id
        else:
            print(f"Response is NOT typed as expected. Type: {type(response)}")

    except Exception as e:
        print(f"Error in get_ds_product: {e}")
    
    return None

def test_query_ds_freight(sku_id):
    if not sku_id:
        return
    print("\n--- Testing query_ds_freight ---")
    product_id = "1005003784285827"
    try:
        # Note: query_ds_freight in CommonMixin currently returns SimpleNamespace as we haven't typed it yet
        # or maybe we did? Let's check common.py
        response = api.query_ds_freight(
            product_id=product_id,
            sku_id=sku_id,
            country_code="US",
            quantity=1,
            language="en"
        )
        print("Successfully retrieved freight info.")
        # If it's SimpleNamespace, it won't be an instance of a model
        print(f"Response type: {type(response)}")
        
    except Exception as e:
        print(f"Error in query_ds_freight: {e}")

def test_get_ds_wholesale_product():
    print("\n--- Testing get_ds_wholesale_product ---")
    product_id = "1005010479059762"
    try:
        # Note: We need to check if get_ds_wholesale_product is typed in Mixin
        response = api.get_ds_wholesale_product(product_id=product_id, country="FR")
        print("Successfully retrieved wholesale product details.")
        print(f"Response type: {type(response)}")
        
    except Exception as e:
         print(f"Error in get_ds_wholesale_product: {e}")

def test_generate_token():
    print("\n--- Testing generate_access_token (Manual Step) ---")
    # This requires a real 'code' from OAuth callback. 
    # Example usage:
    # code = "YOUR_OAUTH_CODE"
    # try:
    #     response = api.generate_access_token(code=code)
    #     print("Token response:", response)
    # except Exception as e:
    #     print(f"Error generating token: {e}")
    print("Skipping token generation test (requires valid code).")

if __name__ == "__main__":
    test_get_ds_categories()
    test_text_search_ds()
    test_get_ds_product()
    test_get_ds_wholesale_product()
    # test_query_ds_freight(sku_id) # freight requires SKU ID which we might not get if products fail
