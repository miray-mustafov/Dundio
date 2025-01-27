from decimal import Decimal
from django.conf import settings
from apps.products.models import Product

example_cart_old = {
    '1': {
        'quantity': 2,
        'price': 100.00
    },
    '2': {
        'quantity': 1,
        'price': 50.00
    },
}
example_cart_with_discounts = {
    'dundio_club_card': 2,  # id
    'promotional_code': 3,  # id
    'products': {
        '1': {
            'quantity': 2,
            'price': 100.00
        },
        '2': {
            'quantity': 1,
            'price': 50.00
        },
    }
}


class Cart:
    DELIVERY_PRICE = 5
    EMPTY_CART = {
        'dundio_club_card': None,
        'promotional_code': None,
        'products': {}
    }

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, Cart.EMPTY_CART)

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart['products']:
            self.cart['products'][product_id] = {  # initialize a new product in the cart
                'quantity': 0, 'price': str(product.price)  # str because decimals cannot be converted directly to json
            }
        if override_quantity:
            self.cart['products'][product_id]['quantity'] = quantity
        else:
            self.cart['products'][product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart['products']:
            del self.cart['products'][product_id]
            self.save()

    def get_total_price_no_discount(self):
        return sum(Decimal(item['price']) * item['quantity']
                   for item in self.cart['products'].values())

    def get_total_discounted_price(self):
        # todo get_discounts func ?
        discount = 0
        return self.get_total_price_no_discount() - discount

    def get_final_price(self):
        return self.get_total_discounted_price() + self._get_delivery_price()

    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def apply_discount(self, dundio_club_card, promo_code):
        if dundio_club_card:
            self._apply_dundio_club_card(dundio_club_card=dundio_club_card)
        elif promo_code:
            self._apply_promo_code(promo_code=promo_code)

    def _apply_dundio_club_card(self, dundio_club_card):
        pass

    def _apply_promo_code(self, promo_code):
        pass

    def _get_delivery_price(self):
        # todo the conditions
        return Cart.DELIVERY_PRICE

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart['products'].keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart['products'].copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            # item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Return the total number of items in the cart.
        """
        return sum(item['quantity'] for item in self.cart['products'].values())
