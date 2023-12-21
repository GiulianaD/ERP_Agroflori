from django.db import models
from datetime import date, datetime
from users.models import User

class SystemTypeCategory(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    def __str__(self) -> str:
        return self.name

class SystemType(models.Model):
    category = models.ForeignKey(SystemTypeCategory, on_delete=models.CASCADE, related_name="category")
    name = models.CharField(max_length=50, blank=False, null=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    unitary_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    def __str__(self) -> str:
        return self.name
    
class Transaction(models.Model):
    CASH = "CA"
    DEBIT_CARD = "DB"
    BANK_TRANSFER = "BT"
    CREDIT_CARD = "CC"
    CHEQUE = "CQ"
    USD = "USD"
    BOB = "BOB"
    INCOME = "IN"
    EXPENDITURE = "EX"

    METHOD_OF_PAYMENT_CHOICES = [
        (CASH, "Cash"),
        (DEBIT_CARD, "Debit card"),
        (CREDIT_CARD, "Credit card"),
        (CHEQUE, "Cheque"),
        (BANK_TRANSFER, "Bank transfer"),
    ]

    CURRENCY_CHOICES = [
        (USD, "American Dollars"),
        (BOB, "Bolivianos")
    ]
    CATEGORY_CHOICES = [
        (INCOME, "Income"),
        (EXPENDITURE, "Expenditure")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_comment="User who registered the transaction.", related_name="user")
    amount = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)
    method_of_payment = models.CharField(max_length=2, choices=METHOD_OF_PAYMENT_CHOICES, default=CASH, null=False, blank=False)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=BOB, null=False, blank=False)
    date = models.DateTimeField(auto_now=False, default= datetime.now, null=False, blank=False)
    description = models.CharField(max_length=300, blank=False, null=False)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, blank=False, null=False)
    
    def __str__(self) -> str:
        return f"{self.date}_{self.category}"
    
class VolunteerPayment(Transaction):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="volunteer")

class Donation(Transaction):
    donor_last_name = models.CharField(max_length=30, blank=False, null=False)
    donor_name  =  models.CharField(max_length=30, blank=False, null=False)

class FoodSale(Transaction):
    pass

class FoodSaleDetail(models.Model):
    food_sale = models.ForeignKey(FoodSale, on_delete=models.CASCADE, related_name="food_sale")
    food_type = models.ForeignKey(SystemType, on_delete=models.CASCADE, related_name="food_type")
    quantity = models.IntegerField(blank=False, null=False, db_comment ="Quantity sold")

class SouvenirSale(Transaction):
    pass

class SouvenirSaleDetail(models.Model):
    souvenir_sale = models.ForeignKey(SouvenirSale, on_delete=models.CASCADE, related_name="souvenir_sale")
    souvenir_type = models.ForeignKey(SystemType, on_delete=models.CASCADE, related_name="souvenir_type")
    quantity = models.IntegerField(blank=False, null=False, db_comment ="Quantity sold")


class TicketSale(Transaction):
    pass

class TicketSaleDetail(models.Model):
    ticket_sale = models.ForeignKey(TicketSale, on_delete=models.CASCADE, related_name="ticket_sale")
    ticket_type = models.ForeignKey(SystemType, on_delete=models.CASCADE, related_name="ticket_type", blank=False)
    quantity = models.IntegerField(blank=False, null=False, db_comment ="Quantity sold")
    promotion_discount = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    promotion_description = models.CharField(max_length=300, blank=True, null=True)


