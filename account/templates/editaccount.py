from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater


def process_request(request):
    

    u = request.user

    form = EditAccountForm(initial = {

        'first_name': '',
        'last_name': '',
        'email': '',
        'street': '',
        'street2': '',
        'city': '',
        'state': '',
        'zipCode': '',
        'phone': '',
        'is_Staff': True,

        })

    if request.method == 'POST':
        form = EditAccountForm(request.POST)
        if form.is_valid():
            u.first_name = form.cleaned_data['first_name']
            u.last_name = form.cleaned_data['last_name']
            u.email = form.cleaned_data['email']
            u.street = form.cleaned_data['street']
            u.street2 = form.cleaned_data['street']
            u.city = form.cleaned_data['city']
            u.state = form.cleaned_data['state']
            u.zipCode = form.cleaned_data['zipCode']
            u.phone = form.cleaned_data['phone']
            u.save()
            return HttpResponseRedirect('/account/accountDashboard/')


            


    template_vars = {
        'form': form,

    }

    return templater.render_to_response(request, 'editaccount.html', template_vars)


class EditAccountForm(forms.Form):


    retype = forms.CharField(widget=forms.PasswordInput())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    street = forms.CharField()
    street2 = forms.CharField(required=False)
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    phone = forms.CharField()
