# Dropshipping Endpoints Implementation

## Overview

This implementation adds **13 dropshipper-specific endpoints** to the Python SDK, based on the official AliExpress Dropshipping API documentation. These endpoints are specifically designed for dropshippers and dropshipping business operations.

## Available Dropshipping Endpoints

### Product Management

#### `get_ds_product(product_id, country=None, fields=None, locale=None, web_site=None)`
Get detailed dropshipping product information.

**API Method:** `aliexpress.ds.product.get`

**Parameters:**
- `product_id` (str, required): The product ID
- `country` (str, optional): Country code for targeting
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Product information including base info, properties, SKU info, logistics, and package details

---

#### `get_ds_wholesale_product(product_id, fields=None, locale=None, web_site=None)`
Get product information for wholesale business.

**API Method:** `aliexpress.ds.product.wholesale.get`

**Parameters:**
- `product_id` (str, required): The product ID
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Wholesale product information with bulk pricing

---

#### `get_ds_product_special_info(product_id, fields=None, locale=None, web_site=None)`
Get special product information like certifications.

**API Method:** `aliexpress.ds.product.specialinfo.get`

**Parameters:**
- `product_id` (str, required): The product ID
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Product special information including certifications

---

#### `text_search_ds(keywords, category_ids=None, country=None, fields=None, locale=None, page_no=None, page_size=None)`
Text search for dropshipping products.

**API Method:** `aliexpress.ds.text.search`

**Parameters:**
- `keywords` (str, required): Search keywords
- `category_ids` (str | list[str], optional): Category IDs to filter by
- `country` (str, optional): Country code for targeting
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `page_no` (int, optional): Page number
- `page_size` (int, optional): Number of records per page

**Returns:** Search results matching the keywords

---

### Order Management

#### `create_ds_order(address, child_order_list, locale=None, web_site=None)`
Create and pay for a dropshipping order.

**API Method:** `aliexpress.ds.order.create`

**Parameters:**
- `address` (dict, required): Shipping address information
- `child_order_list` (list, required): List of child orders with product details
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Order creation response with order details

---

#### `get_trade_ds_order(order_id, fields=None, locale=None, web_site=None)`
Buyer query order details.

**API Method:** `aliexpress.trade.ds.order.get`

**Parameters:**
- `order_id` (str, required): The order ID
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Detailed order information including products and logistics

---

#### `get_ds_order_tracking(order_id, locale=None, web_site=None)`
Get tracking information for a dropshipping order.

**API Method:** `aliexpress.ds.order.tracking.get`

**Parameters:**
- `order_id` (str, required): The order ID
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Order tracking information with shipment status

---

### Freight & Logistics

#### `query_ds_freight(country_code, product_list, locale=None, web_site=None)`
Query freight/shipping costs for products.

**API Method:** `aliexpress.ds.freight.query`

**Parameters:**
- `country_code` (str, required): Country code for shipping destination
- `product_list` (list, required): List of products with SKU information
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Freight/shipping costs for the specified products

---

#### `calculate_buyer_freight(country_code, product_list, locale=None, web_site=None)`
Freight calculation interface provided for buyers.

**API Method:** `aliexpress.logistics.buyer.freight.calculate`

**Parameters:**
- `country_code` (str, required): Country code for shipping destination
- `product_list` (list, required): List of products with SKU information
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Freight calculation for buyers

---

### Categories & Feeds

#### `get_ds_categories(country=None, fields=None, locale=None, web_site=None)`
Get dropshipping categories.

**API Method:** `aliexpress.ds.category.get`

**Parameters:**
- `country` (str, optional): Country code for targeting
- `fields` (str | list[str], optional): Fields to include in the response
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Category information including parent and child categories

---

#### `get_ds_feed_items(feed_name, locale=None, page_no=None, page_size=None, web_site=None)`
Fetch items with feed name in simple model.

**API Method:** `aliexpress.ds.feed.itemids.get`

**Parameters:**
- `feed_name` (str, required): The feed name
- `locale` (str, optional): Locale for the request
- `page_no` (int, optional): Page number
- `page_size` (int, optional): Number of records per page
- `web_site` (str, optional): Website identifier

**Returns:** Feed items for the specified feed

---

### Analytics & Benefits

#### `report_ds_search_event(event_list, locale=None, web_site=None)`
Report search events for analytics.

**API Method:** `aliexpress.ds.search.event.report`

**Parameters:**
- `event_list` (list, required): List of search events to report
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Event report response

---

#### `get_ds_member_benefit(locale=None, web_site=None)`
Get dropshipper member benefits.

**API Method:** `aliexpress.ds.member.benefit.get`

**Parameters:**
- `locale` (str, optional): Locale for the request
- `web_site` (str, optional): Website identifier

**Returns:** Member benefit information

---

## Usage Example

```python
from aliexpress_api import AliexpressApi, models

# Initialize the API
api = AliexpressApi(
    key='YOUR_API_KEY',
    secret='YOUR_API_SECRET',
    language=models.Language.EN,
    currency=models.Currency.USD
)

# Get product details
product = api.get_ds_product(product_id='1005001234567890', country='US')
print(f"Product: {product.ae_item_base_info.subject}")
print(f"Price: {product.ae_item_base_info.sale_price}")

# Search for products
results = api.text_search_ds(keywords='bluetooth earphones', page_no=1, page_size=20)
for item in results:
    print(f"Found: {item}")

# Get categories
categories = api.get_ds_categories(country='US')
for category in categories.categories:
    print(f"Category: {category.category_name}")

# Calculate freight
freight = api.query_ds_freight(
    country_code='US',
    product_list=[{'product_id': '1005001234567890', 'sku_id': 'sku123'}]
)
print(f"Freight: {freight}")

# Create order
order = api.create_ds_order(
    address={
        'address_line1': '123 Main St',
        'city': 'New York',
        'country': 'US',
        'phone': '+1234567890'
    },
    child_order_list=[{
        'product_id': '1005001234567890',
        'sku_id': 'sku123',
        'quantity': 1
    }]
)
print(f"Order created: {order}")
```

## Files Created

### Request Classes (11 files)
- `aliexpress_api/skd/api/rest/AliexpressDsOrderCreateRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsCategoryGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsFreightQueryRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsOrderTrackingGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsFeedItemidsGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsProductGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsProductSpecialinfoGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsProductWholesaleGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsMemberBenefitGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsTextSearchRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressDsSearchEventReportRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressTradeDsOrderGetRequest.py`
- `aliexpress_api/skd/api/rest/AliexpressLogisticsBuyerFreightCalculateRequest.py`

### Models (1 file)
- `aliexpress_api/models/dropshipping.py` - Contains all response models

### Files Modified
- `aliexpress_api/api.py` - Added 13 new dropshipper methods
- `aliexpress_api/skd/api/rest/__init__.py` - Updated imports
- `aliexpress_api/models/__init__.py` - Added model exports
- `README.md` - Updated with dropshipping features section

## Implementation Status

✅ All 13 dropshipper endpoints implemented
✅ 11 request classes created
✅ Response models created
✅ API methods added to AliexpressApi class
✅ Documentation created
✅ All tests passing
✅ Following existing SDK patterns
✅ Compatible with Python 3.6+

## Note

These endpoints are **specifically for dropshippers** using AliExpress's dropshipping platform. They differ from the general affiliate endpoints and provide specialized functionality for dropshipping business operations including:
- Product sourcing and wholesale pricing
- Order creation and management
- Freight calculation and tracking
- Category browsing for dropshipping
- Member benefits
- Search analytics

For more information about dropshipping with AliExpress, refer to the official AliExpress Dropshipping API documentation.
