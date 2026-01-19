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
aliexpress = AliexpressApi(KEY, SECRET, models.Language.EN, models.Currency.EUR, TRACKING_ID)
```

**Get products information:**

```python
products = aliexpress.get_products_details(['1000006468625', 'https://aliexpress.com/item/1005003091506814.html'])
print(products[0].product_title, products[1].target_sale_price)
```

**Get affiliate link:**

```python
affiliate_links = aliexpress.get_affiliate_links('https://aliexpress.com/item/1005003091506814.html')
print(affiliate_links[0].promotion_link)
```

**Get products:**

```python
response = aliexpress.get_products(keywords='bluetooth earphones', max_sale_price=3000)
print(response.products[0].product_title)
```

**Get hotproducts:**

```python
response = aliexpress.get_hotproducts(keywords='bluetooth earphones', max_sale_price=3000)
print(response.products[0].product_main_image_url)
```

**Get categories:**

```python
parent_categories = aliexpress.get_parent_categories()
child_categories = aliexpress.get_child_categories(parent_categories[0].category_id)
```

## Dropshipping Features

The SDK now includes comprehensive dropshipping endpoints. Here are some examples:

**Get dropshipping product details:**

```python
product = aliexpress.get_ds_product(
    product_id='1005001234567890',
    country='US'
)
print(f"Product: {product.ae_item_base_info.subject}")
print(f"Price: {product.ae_item_base_info.sale_price}")
```

**Get dropshipping orders:**

```python
orders = aliexpress.get_ds_orders(
    start_time='2024-01-01 00:00:00',
    end_time='2024-01-31 23:59:59',
    page_no=1,
    page_size=20
)
for order in orders.orders:
    print(f"Order ID: {order.order_id}")
    print(f"Status: {order.order_status}")
```

**Get commission orders:**

```python
commission_orders = aliexpress.get_ds_commission_orders(
    start_time='2024-01-01 00:00:00',
    end_time='2024-01-31 23:59:59'
)
for order in commission_orders.commission_orders:
    print(f"Commission: {order.commission_amount}")
```

For more details on dropshipping endpoints, see [DROPSHIPPING_USAGE.md](DROPSHIPPING_USAGE.md).

## License

Copyright © 2020 Sergio Abad. See [license](https://github.com/sergioteula/python-aliexpress-api/blob/master/LICENSE) for details.
