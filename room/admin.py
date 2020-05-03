from django.contrib import admin
from room.models import AddRoommate, AddExpenses, ExpensePaidAmount, PUBBillAmount

# Register your models here.
class ShowAddRoommate(admin.ModelAdmin):
    list_display = ("id", "date", "name", "phone")

class ShowAddExpenses(admin.ModelAdmin):
    list_display = ("id", "date", "name", "item_name", "item_price")

class ShowExpensePaidAmount(admin.ModelAdmin):
    list_display = ("id", "month_year", "name", "food_expense", "pub", "total_paid_pub")

class ShowPUBBillAmount(admin.ModelAdmin):
    list_display = ("id", "total_units", "refuse_amt", "water_amt", "gst", "total_amt", "food_date")

admin.site.register(AddRoommate, ShowAddRoommate)
admin.site.register(AddExpenses, ShowAddExpenses)
admin.site.register(ExpensePaidAmount, ShowExpensePaidAmount)
admin.site.register(PUBBillAmount, ShowPUBBillAmount)