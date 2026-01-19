from aliexpress_api.api import AliexpressApi, models

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

# 2. Get Dropshipping Categories (Verified Working)
print("\n--- Testing get_ds_categories ---")
try:
    # Get root categories
    categories = api.get_ds_categories(language="en")
    print("Successfully retrieved categories response.")

    # Parse categories
    cats_obj = getattr(categories, "categories", None)
    if not cats_obj and hasattr(categories, "result"):
        cats_obj = getattr(categories.result, "categories", None)

    if cats_obj:
        if hasattr(cats_obj, "category"):
            cats = cats_obj.category
        elif isinstance(cats_obj, list):
            cats = cats_obj
        else:
            cats = []

        if isinstance(cats, list):
            print(f"Found {len(cats)} root categories.")
            if len(cats) > 0:
                c = cats[0]
                name = getattr(c, "category_name", "Unknown")
                cid = getattr(c, "category_id", "Unknown")
                print(f"First category: {name} (ID: {cid})")
        else:
            print(f"Categories structure: {type(cats)}")
    else:
        print("Structure unknown. attributes:", dir(categories))

except Exception as e:
    print(f"Error getting categories: {e}")
    import traceback
    traceback.print_exc()

print("\n--- Testing text_search_ds ---")
try:
    search_result = api.text_search_ds(keywords="watch", country="US", page_size=1)
    print("Successfully retrieved search response.")

    if hasattr(search_result, "products"):
        products = search_result.products
        if isinstance(products, list) and len(products) > 0:
            product = products[0]
            print(f"Found product: {getattr(product, 'product_title', 'Unknown')} (ID: {getattr(product, 'product_id', 'Unknown')})")
        else:
            print("No products found.")
    else:
        print("No products attribute in search result.")

except Exception as e:
    print(f"Error searching products: {e}")

# Hardcoded product ID from user example
product_id = "1005003784285827"
sku_id = None

if product_id:
    print("\n--- Testing get_ds_product ---")
    try:
        product_details = api.get_ds_product(
            product_id=product_id, ship_to_country="US"
        )
        print("Successfully retrieved product details.")

        # Check result structure
        if hasattr(product_details, "product_title"):
            print(f"Product Title: {product_details.product_title}")
            if hasattr(product_details, "ae_item_sku_info_dtos"):
                skus = product_details.ae_item_sku_info_dtos
                if isinstance(skus, list) and len(skus) > 0:
                    sku_info = skus[0]
                    sku_id = getattr(sku_info, "sku_id", None)
                    print(f"Found SKU ID: {sku_id}")
        else:
            print("Product details structure unexpected.")

    except Exception as e:
        print(f"Error getting product details: {e}")

if product_id and sku_id:
    print("\n--- Testing query_ds_freight ---")
    try:
        freight = api.query_ds_freight(
            product_id=product_id,
            sku_id=sku_id,
            country_code="US",
            quantity=1,
            language="en",
        )
        print("Successfully retrieved freight info.")
        if hasattr(freight, "delivery_options"):
            print(f"Found {len(freight.delivery_options)} delivery options.")
    except Exception as e:
        print(f"Error querying freight: {e}")
