# AliExpress API wrapper for Python

A simple Python wrapper for the [AliExpress Open Platform API](https://developers.aliexpress.com/en). This module allows getting information and affiliate links from AliExpress using the official API in an easier way.

[![PyPI](https://img.shields.io/pypi/v/python-aliexpress-api?color=%231182C2&label=PyPI)](https://pypi.org/project/python-aliexpress-api/)
[![Python](https://img.shields.io/badge/Python->3.6-%23FFD140)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-%23e83633)](https://github.com/sergioteula/python-aliexpress-api/blob/master/LICENSE)
[![Support](https://img.shields.io/badge/Support-Good-brightgreen)](https://github.com/sergioteula/python-aliexpress-api/issues)

## Features

- Object oriented interface for simple usage.
- Requests follow the [official documentation](https://developers.aliexpress.com/en/doc.htm?docId=45803&docType=2).
- Ask for new features through the [issues](https://github.com/sergioteula/python-aliexpress-api/issues) section.
- Join our [Telegram group](https://t.me/PythonAliExpressAPI) for support or development.
- **Dropshipping support**: Comprehensive dropshipping endpoints for product management, order tracking, and commission tracking.

## Installation

You can install or upgrade the module with:

    pip install python-aliexpress-api --upgrade

## Usage guide

**Import and initialize the API:**

```python
from aliexpress_api import AliexpressApi, models

# Initialize the API
aliexpress = AliexpressApi(
    key=KEY,
    secret=SECRET,
    language=models.Language.EN,
    currency=models.Currency.EUR,
    tracking_id=TRACKING_ID
)
```

## New Composition-Based API (Recommended)

The SDK now uses a composition-based architecture for better modularity:

**Affiliate operations:**

```python
# Get products information
products = aliexpress.affiliate.get_products_details(['1000006468625'])
print(products[0].product_title)

# Get affiliate links
links = aliexpress.affiliate.get_affiliate_links('https://aliexpress.com/item/123.html')
print(links[0].promotion_link)

# Search products
response = aliexpress.affiliate.get_products(keywords='bluetooth', max_sale_price=3000)
print(response.products[0].product_title)
```

**Dropshipping operations:**

```python
# Get dropshipping product details
product = aliexpress.dropshipping.get_ds_product(
    product_id='1005001234567890',
    ship_to_country='US'
)
print(f"Product: {product.ae_item_base_info.subject}")

# Create order
order = aliexpress.dropshipping.create_ds_order(
    logistics_address={'...': '...'},
    product_items=[{'product_id': '123', 'product_count': 1}]
)
print(f"Order ID: {order.order_id}")

# Get tracking
tracking = aliexpress.dropshipping.get_ds_order_tracking(ae_order_id='12345')
```

**OAuth operations:**

```python
# Generate access token
token = aliexpress.oauth.generate_access_token(code='OAUTH_CODE')
print(f"Access token: {token.access_token}")

# Refresh token
new_token = aliexpress.oauth.refresh_access_token(refresh_token='REFRESH_TOKEN')
```

## Legacy Mixin-Based API (Still Supported)

The old mixin-based API is still fully supported for backward compatibility:

```python
# All methods still work as before
products = aliexpress.get_products_details(['1000006468625'])
links = aliexpress.get_affiliate_links('https://aliexpress.com/item/123.html')
product = aliexpress.get_ds_product('1005001234567890', 'US')
```

## Dropshipping Features

The SDK now includes comprehensive dropshipper-specific endpoints. Here are some examples:

**Get dropshipping product details:**

```python
product = aliexpress.get_ds_product(
    product_id='1005001234567890',
    country='US'
)
print(f"Product: {product.ae_item_base_info.subject}")
print(f"Price: {product.ae_item_base_info.sale_price}")
```

**Search dropshipping products:**

```python
results = aliexpress.text_search_ds(
    keywords='bluetooth earphones',
    country='US',
    page_no=1,
    page_size=20
)
for item in results:
    print(f"Found: {item}")
```

**Calculate freight:**

```python
freight = aliexpress.query_ds_freight(
    country_code='US',
    product_list=[{'product_id': '1005001234567890', 'sku_id': 'sku123'}]
)
print(f"Freight: {freight}")
```

**Get dropshipping categories:**

```python
categories = aliexpress.get_ds_categories(country='US')
for category in categories.categories:
    print(f"Category: {category.category_name}")
```

For more details on dropshipping endpoints, see [DROPSHIPPING_ENDPOINTS.md](DROPSHIPPING_ENDPOINTS.md).

## License

Copyright © 2020 Sergio Abad. See [license](https://github.com/sergioteula/python-aliexpress-api/blob/master/LICENSE) for details.
