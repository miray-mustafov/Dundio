from django.shortcuts import render


def contacts_list_view(request):
    return render(request, 'contacts/contacts.html')
