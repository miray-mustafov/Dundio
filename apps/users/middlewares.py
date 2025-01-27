from apps.users.models import BaseUser, CompanyUser, PhysicalUser


class CustomUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        custom_user_id = request.session.get('custom_user_id')

        request.custom_user = None
        if custom_user_id:
            custom_user = (CompanyUser.objects.filter(id=custom_user_id, is_active=True, is_confirmed=True).first() or
                           PhysicalUser.objects.filter(id=custom_user_id, is_active=True, is_confirmed=True).first())

            request.custom_user = custom_user

        # call the next middleware or the view
        response = self.get_response(request)
        return response
