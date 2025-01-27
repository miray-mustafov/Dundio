from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.db.models import Sum

from apps.promotional_packages.models import PromotionalPackage

"""
    Practice for signals
    Form handling for the price may be better choice
"""


@receiver(m2m_changed, sender=PromotionalPackage.products.through)
@receiver(post_save, sender=PromotionalPackage)
def update_promotional_package_price_m2m(sender, instance, **kwargs):
    """
    This m2m signal also needed because when we add a new package
    the m2m relation is not yet established when post_save signal is triggered.
    """
    calculate_price(instance)


def calculate_price(instance):
    total_price = instance.products.aggregate(total=Sum('price'))['total'] or 0
    if total_price:
        total_price -= instance.you_save
    PromotionalPackage.objects.filter(id=instance.id).update(price=total_price)
