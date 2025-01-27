from apps.products.models import Category
from apps.text_pages.models import FooterMenu
from apps.carts.cart import Cart


def custom_processors(request):
    return {
        'categories': Category.get_active_categories_with_prefetch(),
        'footer_elements_dict': FooterMenu.get_footer_elements_dict(),
        'cart': Cart(request),
    }
