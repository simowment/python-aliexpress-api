"""
Test script for dropshipping endpoints in the Python SDK.
This script demonstrates how to use the new dropshipping endpoints.
"""

from aliexpress_api import AliexpressApi, models


def test_ds_product_get():
    """Test getting dropshipping product details."""
    print("Testing get_ds_product()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        product = api.get_ds_product(
            product_id='1005001234567890',
            country='US'
        )
        print(f"✓ Product retrieved successfully: {product.ae_item_base_info.subject}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_categories():
    """Test getting dropshipping categories."""
    print("\nTesting get_ds_categories()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        categories = api.get_ds_categories(country='US')
        print(f"✓ Retrieved {len(categories.categories)} categories")
        for cat in categories.categories[:3]:
            print(f"  - {cat.category_name} (ID: {cat.category_id})")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_orders():
    """Test getting dropshipping orders."""
    print("\nTesting get_ds_orders()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        orders = api.get_ds_orders(
            start_time='2024-01-01 00:00:00',
            end_time='2024-01-31 23:59:59',
            page_no=1,
            page_size=10
        )
        print(f"✓ Retrieved {len(orders.orders)} orders")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_trade_order():
    """Test getting dropshipping trade order details."""
    print("\nTesting get_ds_trade_order()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        order = api.get_ds_trade_order(order_id='ORDER1234567890')
        print(f"✓ Order retrieved successfully: {order.order_id}")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_commission_orders():
    """Test getting dropshipping commission orders."""
    print("\nTesting get_ds_commission_orders()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        orders = api.get_ds_commission_orders(
            start_time='2024-01-01 00:00:00',
            end_time='2024-01-31 23:59:59',
            page_no=1,
            page_size=10
        )
        print(f"✓ Retrieved {len(orders.commission_orders)} commission orders")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_add_dropshipper():
    """Test adding a new dropshipper."""
    print("\nTesting add_dropshipper()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        result = api.add_dropshipper(
            email='test@example.com',
            mobile='+1234567890',
            app_name='TestApp'
        )
        print(f"✓ Dropshipper added successfully")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_image_search():
    """Test image search for products."""
    print("\nTesting ds_image_search()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        results = api.ds_image_search(
            image_id='test_image_id',
            country='US'
        )
        print(f"✓ Image search completed successfully")
    except Exception as e:
        print(f"✗ Error: {e}")


def test_ds_recommend_feed():
    """Test getting recommended feed products."""
    print("\nTesting get_ds_recommend_feed()...")
    api = AliexpressApi(
        key='YOUR_API_KEY',
        secret='YOUR_API_SECRET',
        language=models.Language.EN,
        currency=models.Currency.USD
    )

    try:
        recommendations = api.get_ds_recommend_feed(
            feed_name='test_feed',
            country='US',
            page_no=1,
            page_size=10
        )
        print(f"✓ Retrieved feed recommendations successfully")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == '__main__':
    print("=" * 60)
    print("AliExpress Python SDK - Dropshipping Endpoints Test")
    print("=" * 60)

    print("\nAvailable dropshipping endpoints:")
    print("  - get_ds_product(): Get dropshipping product details")
    print("  - get_ds_categories(): Get dropshipping categories")
    print("  - get_ds_orders(): List dropshipping orders")
    print("  - get_ds_trade_order(): Get dropshipping trade order details")
    print("  - get_ds_commission_orders(): List commission orders")
    print("  - add_dropshipper(): Add a new dropshipper")
    print("  - ds_image_search(): Search products by image")
    print("  - get_ds_recommend_feed(): Get recommended feed products")

    print("\n" + "=" * 60)
    print("Running tests...")
    print("=" * 60)

    # Run tests
    test_ds_product_get()
    test_ds_categories()
    test_ds_orders()
    test_ds_trade_order()
    test_ds_commission_orders()
    test_add_dropshipper()
    test_ds_image_search()
    test_ds_recommend_feed()

    print("\n" + "=" * 60)
    print("Tests completed!")
    print("=" * 60)
    print("\nNote: Replace 'YOUR_API_KEY' and 'YOUR_API_SECRET' with your")
    print("actual AliExpress API credentials to run real tests.")
