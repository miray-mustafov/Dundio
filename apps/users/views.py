from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from apps.users.forms import RegisterPhysicalUserForm, RegisterCompanyUserForm, LoginUserForm, ForgottenPassForm, \
    ChangePassForm, EditCompanyUserForm, EditPhysicalUserForm, EditPassForm
from apps.common.utils import send_confirmation_email
from apps.users.models import UserConfirmationToken
from apps.users.decorators import custom_login_required, custom_login_forbidden

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.users.models import CompanyUser, PhysicalUser


@custom_login_required
def my_profile_view(request):
    edit_pass_form = EditPassForm()
    user: CompanyUser | PhysicalUser = request.custom_user
    form = EditCompanyUserForm(instance=user) if user.is_company() else EditPhysicalUserForm(instance=user)
    template_name = 'users/my-profile-business.html' if user.is_company() else 'users/my-profile.html'

    if request.method == 'POST':
        if 'editUserForm' in request.POST:
            form = (EditCompanyUserForm(request.POST, instance=user) if user.is_company()
                    else EditPhysicalUserForm(request.POST, instance=user))
            if form.is_valid():
                form.save()
                return redirect(f'{reverse('my-profile')}?useredited=true')
        elif 'editPassForm' in request.POST:
            edit_pass_form = EditPassForm(request.POST)
            if edit_pass_form.is_valid():
                user = request.custom_user
                user.password = edit_pass_form.cleaned_data['new_password']
                user.save()
                return redirect(f'{reverse("index")}?passreset=true')

    context = {'form': form, 'edit_pass_form': edit_pass_form}
    return render(request, template_name, context)


@custom_login_forbidden
def login_view(request):
    form = LoginUserForm()

    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            request.session['custom_user_id'] = form.cleaned_data['custom_user_id']
            return redirect(f'{reverse('index')}?logedin=true')

    return render(request, 'users/login.html', {'form': form})


def _register_form_submission_helper(request, form):
    user = form.save()
    send_confirmation_email(user, request, 'users/email_template_registration_confirmation.html')
    return redirect(f'{reverse('index')}?registered=true')


@custom_login_forbidden
def register_view(request):
    form, company_form = RegisterPhysicalUserForm(), RegisterCompanyUserForm()

    if request.method == 'POST':
        if 'registerPhysicalUserForm' in request.POST:
            form = RegisterPhysicalUserForm(request.POST)
            if form.is_valid():
                return _register_form_submission_helper(request, form)
        elif 'registerCompanyUserForm' in request.POST:
            company_form = RegisterCompanyUserForm(request.POST)
            if company_form.is_valid():
                return _register_form_submission_helper(request, company_form)

    context = {'form': form, 'company_form': company_form}
    return render(request, 'users/registration.html', context)


def check_token_match_view(request):
    """
    Takes token and email from the request url
    Gets confirmation token instance from db, or 404
    Activates the user
    Deactivates the token
    Redirection to login page with confirmed flag
    """
    token = request.GET.get('token')
    email = request.GET.get('email')

    confirmation_token = get_object_or_404(UserConfirmationToken, token=token, user__email=email, is_used=False)

    # activate and confirm the user
    user = confirmation_token.user
    user.is_active = True
    user.is_confirmed = True
    user.save()

    confirmation_token.is_used = True
    confirmation_token.save()

    return redirect(f'{reverse("login")}?confirmed=true')


@custom_login_forbidden
def forgotten_password_view(request):
    form = ForgottenPassForm()
    if request.method == 'POST':
        form = ForgottenPassForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            send_confirmation_email(user, request, 'users/email_template_pass_reset.html')
            return redirect(f'{reverse("index")}?passresetemail=true')

    return render(request, 'users/forgotten-password.html', {'form': form})


def reset_pass_view(request):
    """
    Takes token and email from the request url
    Gets confirmation token instance from db, or 404
    Deactivates the token
    Attaches the user id to session so that the change pass view can access it
    Redirection to change pass page
    """

    form = ChangePassForm()
    if request.method == 'POST':
        form = ChangePassForm(request.POST)
        if form.is_valid():
            confirmation_token = form.cleaned_data.get('confirmation_token')
            user = confirmation_token.user

            confirmation_token.is_used = True
            confirmation_token.save()
            user.password = make_password(form.cleaned_data['new_password'])
            user.save()
            return redirect(f'{reverse("login")}?passreset=true')

    return render(request, 'users/change-password.html', {'form': form})


@custom_login_required
def logout_view(request):
    if 'custom_user_id' in request.session:
        del request.session['custom_user_id']
    return redirect('index')
