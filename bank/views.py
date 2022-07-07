from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Payment
from .models import customer
from django.db.models import F
import decimal
from django.db import transaction

def process_payment(request):

  if request.method == 'POST':

    form = Payment(request.POST)

    if form.is_valid():                                            # form .. the three variables bound to the three input fields in our form on index.html 
      x = form.cleaned_data['payor']                               
      y = form.cleaned_data['payee']                               
      z = decimal.Decimal(form.cleaned_data['amount'])             

      payor = customer.objects.select_for_update().get(name=x)    # retreving the customer whom relates to the input field .. in this case x is payor
      payee = customer.objects.select_for_update().get(name=y)    # y is the payee 

    with transaction.atomic():                                     # minus amount from the payor
      payor.balance -= z
      payor.save()

      payee.balance += z                                          # add amount to payee
      payee.save()

      # customer.objects.filter(name=x).update(balance=F('balance') - z)
      # customer.objects.filter(name=y).update(balance=F('balance') + z)

      return HttpResponseRedirect('/')              

  else:
    form = Payment()

  return render(request, 'index.html', {'form': form})