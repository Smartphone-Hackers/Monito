from django.db import models

# Create your models here.
class AddRoommate(models.Model):
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    date = models.DateField(auto_now=True)

class AddExpenses(models.Model):
    name = models.ForeignKey(AddRoommate, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    item_price = models.FloatField()
    date = models.DateField()

class PUBBillAmount(models.Model):
    date = models.DateField()
    total_units = models.FloatField()
    refuse_amt = models.FloatField()
    water_amt = models.FloatField()
    gst = models.FloatField()
    total_amt = models.FloatField(null=True)
    food_date = models.CharField(max_length=50, null=True)

class ExpensePaidAmount(models.Model):
    month_year = models.CharField(max_length=50)
    name = models.ForeignKey(AddRoommate, on_delete=models.CASCADE)
    no_of_days = models.IntegerField(null=True)
    food_expense = models.FloatField()
    total_paid_pub = models.FloatField(null=True)
    pub = models.ForeignKey(PUBBillAmount, on_delete=models.CASCADE, null=True)
