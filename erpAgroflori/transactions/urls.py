from django.urls import path
from . import views

urlpatterns = [
    path('transaction', views.make_transaction, name="make-transaction"),
    path('ticket', views.register_ticket_sale, name="register-ticket-sale"),
    path('souvenir', views.register_souvenir_sale, name="register-souvenir-sale"),
    path('food', views.register_food_sale, name="register-food-sale"),
    path('search-transaction/', views.TransactionListView.as_view(), name="search-transactions"),
    path('update-transaction/<int:pk>', views.TransactionUpdateView.as_view(), name="update-transaction"),
    path('graphics', views.show_graphics, name="show-graphics"),
    path('get-transaction-details/<int:pk>', views.get_transaction_details, name="get-transaction-details")
]