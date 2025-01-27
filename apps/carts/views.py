import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.cards.models import ClubCard
from apps.carts.forms import ApplyDiscountsForm
from apps.products.models import Product
from apps.carts.cart import Cart
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import CompanyUser, PhysicalUser


@require_POST
def cart_add_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = json.loads(request.body).get('quantity', 1)

    cart = Cart(request)
    cart.add(product=product, quantity=quantity)
    return JsonResponse({'success': True})


@require_POST
def cart_remove_view(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True})


def cart_detail_view(request):
    # todo test
    cart = Cart(request)
    for c in cart:
        print(c)
    apply_discounts_form = ApplyDiscountsForm()

    user: CompanyUser | PhysicalUser = request.custom_user
    if request.method == 'POST':
        apply_discounts_form = ApplyDiscountsForm(request.POST)
        if apply_discounts_form.is_valid():
            dundio_club_card = apply_discounts_form.cleaned_data['dundio_club_card']
            promo_code = apply_discounts_form.cleaned_data['promo_code']
            cart.apply_discount(dundio_club_card=dundio_club_card, promo_code=promo_code)

    dundio_club_card = None  # todo add that club card to the session and maybe its number
    context = {'cart': cart, 'apply_discounts_form': apply_discounts_form, 'dundio_club_card': dundio_club_card}
    return render(request, 'carts/shopping-cart.html', context)
