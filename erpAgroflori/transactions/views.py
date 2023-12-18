from django.shortcuts import render, redirect
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.db.models import Q

# Create your views here.
def make_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, **{'user':request.user})
        if form.is_valid():
            form.save(commit=True)
    else:
        form = TransactionForm()
    return render(request, "transaction.html", {"form": form})
    
def register_ticket_sale(request):
    if request.method == 'POST':
        sale_form = TicketSaleForm(request.POST, **{'user':request.user})
        formset = TicketSaleFormSet(request.POST)
        
        if sale_form.is_valid():
            ticket_sale = sale_form.save(commit=True)
            ticket_sale.transaction_ptr.category = "IN"
            ticket_sale.transaction_ptr.description = f"Venta de entradas {ticket_sale.date}"
            ticket_sale.transaction_ptr.save()
            formset = TicketSaleFormSet(request.POST, instance=ticket_sale)
            if formset.is_valid():
                formset.save()
            else:
                TicketSale.objects.filter(id=sale_form.id).delete()
            return redirect('home')
        else:
            # Print or log form errors
            print("Form is not valid:", sale_form.errors)
    else:
        sale_form = TicketSaleForm()
        formset=TicketSaleFormSet()
    return render(request, 'ticket.html', {'sale_form': sale_form, 'formset': formset})
    

def register_souvenir_sale(request):
    if request.method == 'POST':
        sale_form = SouvenirSaleForm(request.POST, **{'user':request.user})
        formset = SouvenirSaleFormSet(request.POST)
        
        if sale_form.is_valid():
            souvenir_sale = sale_form.save(commit=True)
            souvenir_sale.transaction_ptr.category = "IN"
            souvenir_sale.transaction_ptr.description = f"Souvenir sale {souvenir_sale.date}"
            souvenir_sale.transaction_ptr.save()
            formset = SouvenirSaleFormSet(request.POST, instance=souvenir_sale)
            if formset.is_valid():
                formset.save()
            else:
                SouvenirSale.objects.filter(id=sale_form.id).delete()
            return redirect('home')
        else:
            # Print or log form errors
            print("Form is not valid:", sale_form.errors)
    else:
        sale_form = SouvenirSaleForm()
        formset=SouvenirSaleFormSet()
    return render(request, 'souvenir.html', {'sale_form': sale_form, 'formset': formset})

def register_food_sale(request):
    if request.method == 'POST':
        sale_form = FoodSaleForm(request.POST, **{'user':request.user})
        formset = FoodSaleFormSet(request.POST)
        
        if sale_form.is_valid():
            food_sale = sale_form.save(commit=True)
            food_sale.transaction_ptr.category = "IN"
            food_sale.transaction_ptr.description = f"Food sale {food_sale.date}"
            food_sale.transaction_ptr.save()
            formset = FoodSaleFormSet(request.POST, instance=food_sale)
            if formset.is_valid():
                formset.save()
            else:
                FoodSale.objects.filter(id=sale_form.id).delete()
            return redirect('home')
        else:
            # Print or log form errors
            print("Form is not valid:", sale_form.errors)
    else:
        sale_form = FoodSaleForm()
        formset=FoodSaleFormSet()
    return render(request, 'food.html', {'sale_form': sale_form, 'formset': formset})
class TransactionListView(ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "transaction_list.html"
    paginate_by = 10 

    def get_queryset(self):
        queryset = Transaction.objects.all()  # Initial queryset
        if (self.request.GET.get('datepicker1') is not None):
            start_date = self.request.GET.get('datepicker1')
            end_date = self.request.GET.get('datepicker2')
            queryset = Transaction.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date))
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datepicker1'] = self.request.GET.get('datepicker1', '')
        context['datepicker2'] = self.request.GET.get('datepicker2', '')
        return context
    
class TransactionUpdateView(UpdateView):
    model = Transaction
    fields = '__all__'
    template_name = "transaction_update_form.html"
    success_url = reverse_lazy("search-transactions")
       

def get_transaction_details(request, pk):
    try:
        ticket_sale_detail = TicketSaleDetail.objects.filter(ticket_sale_id=pk)
        if ticket_sale_detail.exists():
            return render(request, 'ticket_details.html', {'transaction_details': ticket_sale_detail})
    except TicketSaleDetail.DoesNotExist:
        pass

    try:
        food_sale_detail = FoodSaleDetail.objects.filter(food_sale_id=pk)
        if food_sale_detail.exists():
            return render(request, 'food_details.html', {'transaction_details': food_sale_detail})
    except FoodSaleDetail.DoesNotExist:
        pass

    try:
        souvenir_sale_detail = SouvenirSaleDetail.objects.filter(souvenir_sale_id=pk)
        if souvenir_sale_detail.exists():
             return render(request, 'souvenir_details.html', {'transaction_details': souvenir_sale_detail})
    except SouvenirSaleDetail.DoesNotExist:
        pass
    return redirect('search-transactions')