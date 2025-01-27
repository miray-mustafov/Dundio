from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from apps.promo_codes.models import PromoCodeGenerator, PromoCode

ALLOWED_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


@receiver(post_save, sender=PromoCodeGenerator)
def create_codes_signal(sender, instance: PromoCodeGenerator, created, **kwargs):
    """
    Creates promo code records based on the sender code generator
    """

    # ensure codes are created only when the generator is initialized
    if not created:
        return

    for _ in range(instance.count):
        PromoCode.objects.create(
            title=get_random_string(length=8, allowed_chars=ALLOWED_CHARS),
            generator=instance,
            discount_type=instance.discount_type,
            discount_value=instance.discount_value,
            valid_to_date=instance.valid_to_date,
            valid_from_date=instance.valid_from_date,
        )


''' bulk_create attempt for educational purposes:

@receiver(post_save, sender=PromoCodeGenerator)
def create_codes_signal(sender, instance: PromoCodeGenerator, created, **kwargs):
    def id_generator(initial_id, count):
        cur_id = initial_id + 1
        for _ in range(count):
            yield cur_id
            cur_id += 1
            
    try: # handling needed bcs .latest is not safe function
        previous_id = PromoCode.objects.latest('id').id
    except PromoCode.DoesNotExist:
        previous_id = 0

    id_gen = id_generator(previous_id, instance.count)
    codes = [
        PromoCode(
            id=next(id_gen), # concisely generating id dynamically with that generator
            title=get_random_string(length=8, allowed_chars=ALLOWED_CHARS),
            #...
        ) for _ in range(instance.count)
    ]
    PromoCode.objects.bulk_create(codes)  # create multiple records at once with single db query
    # MUST update the id autoincrement counter
'''
