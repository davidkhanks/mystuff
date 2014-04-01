from django import forms
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from homepage.models import *
from manager import models as mmod
from . import templater
from random import randint
from datetime import datetime


def process_request(request):
    '''Get products from the DB'''
    user = mmod.User.objects.get(id=request.urlparams[0])
    request.session['current_user'] = 'None'
    request.session['current_user'] = user.id
    request.session['rental'] = 'None'
    rentalcart = request.session.get('rentalcart', {})
    catalog = mmod.CatalogInventory.objects.all()
    products = []
    error_code = 0

    for key in rentalcart:
        prod = mmod.Product.objects.get(id=key)
        products.append(prod)

    form = CardForm()

    if request.method == 'POST':
        form = TermsForm(request.POST)
        if form.is_valid():
            # begin_date = form.cleaned_data['begin_date']
            # end_date = form.cleaned_data['end_date']

            # print('>>>>>>>>>>>>>>>>>>>>>>>' + str(begin_date))
            # print('>>>>>>>>>>>>>>>>>>>>>>>' + str(end_date))

            # if end_date < begin_date:
            #     error_code = 1

            # if error_code == 0:
            #     r = mmod.Rental()
            #     r.dateOut = form.cleaned_data['begin_date']
            #     r.dateDue = form.cleaned_data['end_date']
            #     # r.dateIn = None
            #     r.work_order = randint(10000,1000000)
            #     r.user_id = user.id
            #     r.save()
            #     request.session['rental'] = r.id

            #     for p in products:
            #         ri = mmod.RentalItem()
            #         ri.rental_id = r.id
            #         ri.product_id = p.id
            #         ri.save()

            #         p.rented_out = True
            #         p.times_rented += 1
            #         p.save()
            # return HttpResponseRedirect('/rental/rentalreceipt')


    template_vars = {
        'user': user,
        'form': form,
        'products': products,
        'catalog': catalog,
        'error_code': error_code,
    }

    return templater.render_to_response(request, 'rental_checkout.html', template_vars)

class CardForm(forms.Form):
    '''The billing address form'''
    card_number = forms.CharField()
    cvn = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    street = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zipCode = forms.CharField()
    exp_date = forms.DateField(widget=forms.TextInput(attrs={'id':'datepicker'}))