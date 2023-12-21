from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.forms import inlineformset_factory
from .forms import *
from .models import *
from django.db.models import Q, Avg, Count, Sum
import plotly.express as px
from datetime import datetime, timedelta

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

def count_tickets(request):
    current_date = datetime.now()
    start_date = request.GET.get('datepicker1', current_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('datepicker2', current_date.strftime('%Y-%m-%d'))

    ticket_sale_ids = Transaction.objects.filter(Q(date__date__gte=start_date) & Q(date__date__lte=end_date)).values_list('id', flat=True)

    system_type_dict = SystemType.objects.values('id', 'name').order_by('id')
    system_type_dict = {item['id']: item['name'] for item in system_type_dict}

    result_dict = {}

    for system_type_id, system_type_name in system_type_dict.items():
        total_quantity = 0

        for ticket_id in ticket_sale_ids:

            quantity_for_ticket = TicketSaleDetail.objects.filter(ticket_type=system_type_id, ticket_sale_id=ticket_id).aggregate(total_quantity=Sum('quantity'))['total_quantity']

            if quantity_for_ticket is not None:
                total_quantity += quantity_for_ticket

        if total_quantity != 0:
            result_dict[system_type_name] = total_quantity

    fig = px.pie(values=result_dict.values(), names=result_dict.keys(), title='Entradas Vendidas')

    chart = fig.to_html()
    return chart

def count_food(request):
    current_date = datetime.now()
    start_date = request.GET.get('datepicker3', current_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('datepicker4', current_date.strftime('%Y-%m-%d'))

    sale_ids = Transaction.objects.filter(Q(date__date__gte=start_date) & Q(date__date__lte=end_date)).values_list('id', flat=True)

    system_type_dict = SystemType.objects.values('id', 'name').order_by('id')
    system_type_dict = {item['id']: item['name'] for item in system_type_dict}

    result_dict = {}

    for system_type_id, system_type_name in system_type_dict.items():
        total_quantity = 0

        for id in sale_ids:

            quantity = FoodSaleDetail.objects.filter(food_type=system_type_id, food_sale_id=id).aggregate(total_quantity=Sum('quantity'))['total_quantity']

            if quantity is not None:
                total_quantity += quantity

        if total_quantity != 0:
            result_dict[system_type_name] = total_quantity

    print(result_dict)
    fig = px.pie(values=result_dict.values(), names=result_dict.keys(), title='Comida Vendida')

    chart = fig.to_html()
    
    return chart

def count_souvenirs(request):
    current_date = datetime.now()
    start_date = request.GET.get('datepicker5', current_date.strftime('%Y-%m-%d'))
    end_date = request.GET.get('datepicker6', current_date.strftime('%Y-%m-%d'))

    sale_ids = Transaction.objects.filter(Q(date__date__gte=start_date) & Q(date__date__lte=end_date)).values_list('id', flat=True)

    system_type_dict = SystemType.objects.values('id', 'name').order_by('id')
    system_type_dict = {item['id']: item['name'] for item in system_type_dict}

    result_dict = {}

    for system_type_id, system_type_name in system_type_dict.items():
        total_quantity = 0

        for id in sale_ids:

            quantity = SouvenirSaleDetail.objects.filter(souvenir_type=system_type_id, souvenir_sale_id=id).aggregate(total_quantity=Sum('quantity'))['total_quantity']

            if quantity is not None:
                total_quantity += quantity

        if total_quantity != 0:
            result_dict[system_type_name] = total_quantity

    fig = px.pie(values=result_dict.values(), names=result_dict.keys(), title='Souvenirs Vendidos')

    chart = fig.to_html()
    
    return chart

def show_graphics(request):
    tickets_chart = count_tickets(request)
    food_chart = count_food(request)
    souvenirs_chart = count_souvenirs(request)

    context = {
        'ticketChart': tickets_chart,
        'foodChart': food_chart,
        'souvenirChart': souvenirs_chart,
    }

    return render(request, 'graphics.html', context)

def view_profile(request):
    return render(request, 'profile.html')

class TransactionListView(ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "transaction_list.html"
    paginate_by = 10 

    def get_queryset(self):
        queryset = Transaction.objects.all()  # Initial queryset
        if (self.request.GET.get('datepicker1') is not None):
            start_date = self.request.GET.get('datepicker1')
   
            # Obtener 'end_date' como string desde la request
            end_date_str = self.request.GET.get('datepicker2')

            # Convertir 'end_date_str' a un objeto datetime
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            # Sumar un día a 'end_date'
            end_date += timedelta(days=1)

            # Convertir 'end_date' de nuevo a string
            end_date_str_updated = end_date.strftime('%Y-%m-%d')

            queryset = Transaction.objects.filter(Q(date__gte=start_date) & Q(date__lte=end_date_str_updated))
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
