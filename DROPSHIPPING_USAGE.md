# Dropshipping Endpoints Usage Guide

This guide shows how to use the new dropshipping endpoints in the Python SDK.

## Initialization

```python
from aliexpress_api import AliexpressApi, models

aliexpress = AliexpressApi(
    key='YOUR_API_KEY',
    secret='YOUR_API_SECRET',
    language=models.Language.EN,
    currency=models.Currency.USD,
    tracking_id='YOUR_TRACKING_ID'
)
```

## Dropshipping Product Operations

### Get Dropshipping Product Details

Get detailed information about a dropshipping product:

```python
# Get product details
product_info = aliexpress.get_ds_product(
    product_id='1005001234567890',
    country='US',
    web_site='US'
)

print(f"Product ID: {product_info.ae_item_base_info.product_id}")
print(f"Title: {product_info.ae_item_base_info.subject}")
print(f"Price: {product_info.ae_item_base_info.sale_price}")
print(f"Stock: {product_info.ae_item_base_info.inventory}")
```

### Get Dropshipping Categories

Get dropshipping categories:

```python
# Get all dropshipping categories
categories = aliexpress.get_ds_categories(
    country='US',
    web_site='US'
)

for category in categories.categories:
    print(f"Category ID: {category.category_id}")
    print(f"Category Name: {category.category_name}")
    if category.children:
        for child in category.children:
            print(f"  Child: {child.category_name}")
```

### Image Search

Search for products using an image:

```python
# Search products by image
search_results = aliexpress.ds_image_search(
    image_id='your_image_id',
    country='US',
    web_site='US'
)

# Process search results
```

### Get Recommended Feed Products

Get recommended products from a feed:

```python
# Get recommended feed products
recommendations = aliexpress.get_ds_recommend_feed(
    feed_name='your_feed_name',
    country='US',
    page_no=1,
    page_size=20,
    web_site='US'
)

# Process recommendations
```

## Dropshipping Order Operations

### Get Dropshipping Orders

List dropshipping orders within a time range:

```python
from datetime import datetime, timedelta

# Calculate time range
end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
start_time = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

# Get orders
orders = aliexpress.get_ds_orders(
    start_time=start_time,
    end_time=end_time,
    status='IN_PROGRESS',
    page_no=1,
    page_size=20
)

for order in orders.orders:
    print(f"Order ID: {order.order_id}")
    print(f"Status: {order.order_status}")
    print(f"Total: {order.total_amount}")
    print(f"Products: {order.product_count}")
```

### Get Dropshipping Trade Order Details

Get detailed information about a specific order:

```python
# Get order details
order_details = aliexpress.get_ds_trade_order(
    order_id='ORDER1234567890'
)

print(f"Order ID: {order_details.order_id}")
print(f"Status: {order_details.order_status}")
print(f"Total Amount: {order_details.total_amount}")

for product in order_details.order_products:
    print(f"Product: {product.product_name}")
    print(f"Quantity: {product.product_count}")
    print(f"Price: {product.product_price}")
```

### Get Dropshipping Commission Orders

Get commission orders within a time range:

```python
# Get commission orders
commission_orders = aliexpress.get_ds_commission_orders(
    start_time=start_time,
    end_time=end_time,
    page_no=1,
    page_size=20
)

for order in commission_orders.commission_orders:
    print(f"Order ID: {order.order_id}")
    print(f"Commission Status: {order.commission_status}")
    print(f"Commission Rate: {order.commission_rate}")
    print(f"Commission Amount: {order.commission_amount}")
```

## Dropshipper Management

### Add a New Dropshipper

Add a new dropshipper to your account:

```python
# Add a new dropshipper
result = aliexpress.add_dropshipper(
    email='dropshipper@example.com',
    mobile='+1234567890',
    app_name='MyApp',
    country='US',
    platform='web'
)

print("Dropshipper added successfully!")
```

## Available Dropshipping Endpoints

### Product Operations
- `get_ds_product()` - Get detailed dropshipping product information
- `get_ds_categories()` - Get dropshipping categories
- `ds_image_search()` - Search products by image
- `get_ds_recommend_feed()` - Get recommended feed products

### Order Operations
- `get_ds_orders()` - List dropshipping orders
- `get_ds_trade_order()` - Get detailed trade order information
- `get_ds_commission_orders()` - List commission orders

### Dropshipper Operations
- `add_dropshipper()` - Add a new dropshipper

## Response Models

### DsProductGetResponse
Contains:
- `ae_item_base_info` - Basic product information
- `ae_item_property` - Product properties
- `ae_item_sku_info` - SKU information
- `logistics_info` - Shipping/logistics information
- `package_info` - Package dimensions
- `multimedia_info` - Videos and images

### DsCategoryGetResponse
Contains:
- `categories` - List of categories with parent/child relationships

### DsOrderListResponse
Contains:
- `orders` - List of orders with basic information

### DsTradeOrderGetResponse
Contains:
- Order details including products and logistics information

### DsCommissionOrderListResponse
Contains:
- `commission_orders` - List of commission orders with earnings

## Error Handling

All dropshipping endpoints can raise the following exceptions:

```python
from aliexpress_api.errors import (
    ProductsNotFoudException,
    OrdersNotFoundException,
    ApiRequestException,
    ApiRequestResponseException
)

try:
    product = aliexpress.get_ds_product(product_id='1005001234567890')
except ProductsNotFoudException:
    print("Product not found")
except ApiRequestException as e:
    print(f"API request failed: {e}")
except ApiRequestResponseException as e:
    print(f"API response error: {e}")
```

## Best Practices

1. **Pagination**: Always use pagination when listing orders or products
2. **Time Ranges**: Keep time ranges reasonable (max 90 days recommended)
3. **Error Handling**: Always wrap API calls in try-except blocks
4. **Caching**: Cache category data to reduce API calls
5. **Rate Limiting**: Respect API rate limits to avoid being throttled

## Notes

- Dropshipping endpoints require appropriate API permissions
- Some endpoints may require additional authentication or special access
- Always refer to the official AliExpress documentation for the most up-to-date API specifications
