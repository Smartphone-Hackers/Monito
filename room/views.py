from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from room.forms import AddRoommateForm
from room.models import AddRoommate, AddExpenses, ExpensePaidAmount, PUBBillAmount
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from calendar import monthrange

# Create your views here.
class Dashboard(View):
    template_name = "index.html"
    def get(self, request):
        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12,}

        get_month = request.GET.get("month")

        roommates_exp = ExpensePaidAmount.objects.all().last()
        roommate = AddRoommate.objects.all().count()
        
        if roommates_exp:
            roommates_expense = ExpensePaidAmount.objects.filter(month_year=roommates_exp.month_year)    
            p = PUBBillAmount.objects.filter(food_date=roommates_exp.month_year)
            if roommate != 0:
                pub_amt = p.first().total_amt/roommate if p else 0
                last_month_expense = AddExpenses.objects.filter(date__year=str(roommates_exp.month_year).split()[1]).filter(date__month=months.get(str(roommates_exp.month_year).split()[0])).aggregate(Sum("item_price"))["item_price__sum"]
                index_pub_total = p.first().total_amt if p else 0

            if p:
                for r in roommates_expense:
                    r.total_paid_pub = r.food_expense + pub_amt
                    r.save()
        else:
            roommates_expense = ""
            pub_amt = 0
            if roommate == 0:
                roommate = 0
            last_month_expense = 0
            index_pub_total = 0

        context = {
            "datas": roommates_expense,
            "last_date": roommates_exp,
            "pub_amt": pub_amt,
            "roommate": roommate,
            "last_month_expense": last_month_expense,
            "index_pub_total": index_pub_total,
        }
        return render(request, template_name=self.template_name, context=context)

class AddRoomies(View):
    template_name='add_roomies.html'
    def get(self, request):
        room = AddRoommate.objects.all()
        context = {
            "room": room,
        }
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        room = AddRoommate(name=name, phone=phone)
        room.save()
        messages.info(request, "Roommate Added")
        return redirect("/addroomate")

class AddRoomiesEdit(View):
    template_name = 'add_roomies.html'
    def get(self, request, pk):
        room = AddRoommate.objects.get(id=pk)
        context = {
            "rooms": room,
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, pk):
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        room = AddRoommate.objects.get(id=pk)
        room.name = name
        room.phone = phone
        room.save()
        messages.info(request, "Edited Data Updated")
        return redirect("/addroomate")

class AddRoomiesDelete(View):
    def get(self, request, pk):
        room = AddRoommate.objects.get(id=pk)
        room.delete()
        return redirect("/addroomate")

class AddExpense(View):
    template_name="add_expense.html"
    def get(self, request):
        roommates = AddRoommate.objects.all()
        expenses = AddExpenses.objects.filter(date__year=date.today().year).filter(date__month=date.today().month)
        this_month_expense = AddExpenses.objects.filter(date__month=date.today().month).aggregate(Sum("item_price"))["item_price__sum"]
        x = round(this_month_expense, 2) if this_month_expense is not None else this_month_expense
        context = {
            "datas": roommates,
            "expenses": expenses,
            "this_month_expense": x,
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        name = request.POST.get("name")
        date = request.POST.get("date")
        item_name = request.POST.get("item_name")
        item_price = request.POST.get("item_price")
        roommate = AddRoommate.objects.filter(name=name)
        if roommate:
            print(name, item_name, item_price, roommate)
            add_expense = AddExpenses(name=roommate.first(), item_name=item_name, item_price=item_price, date=date)
            add_expense.save()
            messages.info(request, "Data Update Successfully.")
            return redirect("/add-expense")
        else:
            messages.info(request, "Sorry! Something Wrong.")
            return redirect("/add-expense")

class AddExpenseEdit(View):
    template_name = "add_expense.html"
    def get(self, request, pk):
        roommates = AddRoommate.objects.all()
        expenses = AddExpenses.objects.get(id=pk)
        expense_date = expenses.date.strftime('%Y-%m-%d') #Date Formate - 2020-04-03
        context = {
            "expense": expenses,
            "expense_date": expense_date,
            "datas": roommates,
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, pk):
        name = request.POST.get("name")
        date = request.POST.get("date")
        item_name = request.POST.get("item_name")
        item_price = request.POST.get("item_price")
        roommate = AddRoommate.objects.filter(name=name)
        if roommate:
            add_expense = AddExpenses.objects.get(id=pk)
            add_expense.name = roommate.first()
            add_expense.date = date
            add_expense.item_name = item_name
            add_expense.item_price = item_price
            add_expense.save()
        return redirect("/add-expense")


class AddExpenseDelete(View):
    template_name = "add_expense.html"
    def get(self, request, pk):
        expenses = AddExpenses.objects.get(id=pk)
        expenses.delete()
        return redirect("/add-expense")

clicked_month = {}

class CalculteExpense(View):
    template_name = "calculate_expense.html"
    def get(self, request):
        self.get_month = request.GET.get("month")
        if self.get_month is not None:
            clicked_month["month"] = self.get_month

        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                  "September": 9, "October": 10, "November": 11, "December": 12,}
        given_month = date(date.today().year, months.get(clicked_month.get("month"), date.today().month), 1)
        this_month_expense = AddExpenses.objects.filter(date__year=given_month.year).filter(date__month=given_month.month).aggregate(Sum("item_price"))["item_price__sum"]
        this_month_expense = this_month_expense if this_month_expense is not None else 0
        roommates = AddRoommate.objects.all()
        if roommates.count() != 0:
            per_day = (this_month_expense/roommates.count())/monthrange(given_month.year, given_month.month)[1]
        else:
            per_day = 0
        last_month = monthrange(given_month.year, given_month.month)[1]

        no_of_days = request.GET.getlist("no_of_days")
        absent_roomies = [ per_day*(last_month-int(i)) for i in no_of_days if int(i) < last_month ]
        absent_roomies_amt, no_of_absent = sum(absent_roomies), len(absent_roomies)
        amt_to_paid = []
        for i in no_of_days:
            if int(i) == last_month:
                if roommates.count() != 0:
                    amt_to_paid.append((per_day*int(i)) + (absent_roomies_amt/(abs(roommates.count()-no_of_absent))))
            else:
                amt_to_paid.append(per_day*int(i))

        extract_roommate = [ i.name for i in roommates ]
        roommate_amt = [ i for i in zip(extract_roommate, no_of_days, [ round(i, 2) for i in amt_to_paid ]) ]

        if round(this_month_expense, 2) != round(sum(amt_to_paid), 2) and round(sum(amt_to_paid), 2) != 0:
            messages = "Total Expense Not Equal - $ {}".format(sum(amt_to_paid))
        else:
            messages = ""

        #insert data to ExpensePaidAmount
        if (len(extract_roommate) != 0) and (len(no_of_days) != 0) and (len(amt_to_paid) != 0) and (clicked_month.get("month") is not None):
            for data in zip(extract_roommate, no_of_days, amt_to_paid):
                person = AddRoommate.objects.get(name=data[0])
                check_month_year = ExpensePaidAmount.objects.filter(month_year=str(clicked_month["month"]) + " " + str(date.today().year)).filter(name=person)
                
                if check_month_year:
                    month_year = str(clicked_month["month"]) + " " + str(date.today().year)
                    person = AddRoommate.objects.get(name=data[0])
                    x = check_month_year.first()
                    x.month_year = month_year
                    x.name = person
                    x.no_of_days = data[1]
                    x.food_expense = data[2]
                    x.save()
                    print("Exist Data")
                else:
                    month_year = str(clicked_month["month"]) + " " + str(date.today().year)
                    person = AddRoommate.objects.get(name=data[0])
                    x = ExpensePaidAmount(month_year=month_year, name=person, no_of_days=data[1], food_expense=data[2])
                    x.save()
                    print("New Data")

        context = {
            "months": months,
            "year": date.today().year,
            "roommates": roommates,
            "get_month": clicked_month.get("month"),
            "this_month_expense": round(this_month_expense, 2),
            "per_day": round(per_day, 2),
            "last_month": last_month,
            "roommate_amt": roommate_amt,
            "messages": messages,
        }
        return render(request, template_name=self.template_name, context=context)

class PubBill(View):
    template_name = "pub_bill.html"
    def get(self, request):
        pubbill = PUBBillAmount.objects.all()[::-1]
        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                  "September": 9, "October": 10, "November": 11, "December": 12,}
        
        month = request.GET.get("month")
        if month is not None:
            # amt = ExpensePaidAmount.objects.all()
            m = PUBBillAmount.objects.get(id=int(month[-1]))
            month_year = month[:-1] + " " + str(date.today().year)
            m.food_date = month_year
            m.save()

        context = {
            "pubbill": pubbill,
            "months": months,
            "year": date.today().year
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        eb_date = request.POST.get("eb_date")
        total_units = request.POST.get("total_units")
        removal_amt = request.POST.get("removal_amt")
        water_amt = request.POST.get("water_amt")
        gst = request.POST.get("gst")
        
        print(eb_date, total_units, removal_amt, water_amt, gst)

        total = (float(total_units) * 0.1495) + float(removal_amt) + float(water_amt)
        add_gst = (total * 7)/100
        total = total + add_gst
        
        bill = PUBBillAmount(date=eb_date, total_units=total_units, refuse_amt=removal_amt, water_amt=water_amt, gst=gst, total_amt=total)
        bill.save()
        return redirect("/pub-bill")

class PubBillEdit(View):
    template_name = "pub_bill.html"
    def get(self, request, pk):
        get_bill = PUBBillAmount.objects.get(id=pk)
        bill_date = get_bill.date.strftime('%Y-%m-%d') #Date Formate - 2020-04-03
        context = {
            "get_bill": get_bill,
            "bill_date": bill_date,
        }
        return render(request, template_name=self.template_name, context=context)
    def post(self, request, pk):
        get_bill = PUBBillAmount.objects.get(id=pk)
        eb_date = request.POST.get("eb_date")
        total_units = request.POST.get("total_units")
        removal_amt = request.POST.get("removal_amt")
        water_amt = request.POST.get("water_amt")
        gst = request.POST.get("gst")

        get_bill.date = eb_date
        get_bill.total_units = total_units
        get_bill.refuse_amt = removal_amt
        get_bill.water_amt = water_amt
        get_bill.gst = gst

        # PUB Total Amount Calculation
        total = (float(total_units)*0.1495) + float(removal_amt) + float(water_amt)
        add_gst = (total * 7)/100
        total = total + add_gst
        get_bill.total_amt = total
        get_bill.save()
        return redirect("/pub-bill")

class PubBillDelete(View):
    template_name="pub-bill.html"
    def get(self, request, pk):
        d = PUBBillAmount.objects.get(id=pk)
        d.delete()
        return redirect("/pub-bill")