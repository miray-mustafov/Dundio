from django.shortcuts import render
from apps.common.models import SubscribedNewsletterEmail
from django.http import JsonResponse


def index_view(request):
    return render(request, 'common/index.html')


def subscribe_newsletter_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        instance = SubscribedNewsletterEmail.objects.filter(email=email).first()
        if instance:
            # Return JSON response for already subscribed
            return JsonResponse({'status': 'already_subscribed'})

        # Create new subscription
        SubscribedNewsletterEmail.objects.create(email=email)
        return JsonResponse({'status': 'subscribed'})

    return JsonResponse({'status': 'error'}, status=400)
