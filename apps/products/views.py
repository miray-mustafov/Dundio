from django.db.models import Q
from django.http import response
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
import json

from apps.cards.models import ClubCard
from apps.common.utils import request_is_ajax
from apps.products.models import Product, Category, Producer
from django.http import JsonResponse
from django.template.loader import render_to_string


def products_view(request, slug):
    category = Category.objects.filter(slug=slug).first()
    if category:
        products = Product.objects.filter(is_active=True, category=category)
    else:
        return redirect('index')

    context = {
        'products': products,
        'category': category,
        'category_ancestors': category.get_ancestors,
        'producers': Producer.objects.filter(is_active=True),
    }
    return render(request, 'products/products.html', context=context)


def product_details_view(request, slug):
    # Prefetch('freq_bought_together', queryset=Product.objects.all()[:3]), )
    product = (Product.objects.filter(is_active=True, slug=slug)
               .prefetch_related('images', 'files', 'related_products', 'freq_bought_together')
               .select_related('category').first())

    if product:
        context = {'product': product}
        return render(request, 'products/product_details.html', context=context)

    return response.HttpResponseNotFound()


def products_search_view(request):
    query = request.GET.get('q')

    products = Product.objects.none()
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        )

    # Check if the request is ajax to do the autocomplete logic
    if request_is_ajax(request):
        products = products[:4]  # add limit to the query

        # Render the products into a html string using a template
        html = render_to_string('products/partials/_search_autocomplete_results.html', {'products': products})
        return JsonResponse({'success': True, 'html': html})

    context = {
        'products': products,
        'page_title': f'Резултати за {query}' if query else 'Няма резултати',
    }
    return render(request, 'products/search.html', context)
