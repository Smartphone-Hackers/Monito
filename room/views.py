from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, UpdateView
from room.forms import AddRoommateForm
from room.models import AddRoommate, AddExpenses, ExpensePaidAmount, PUBBillAmount
from django.contrib import messages
from django.db.models import Sum
from datetime import date
from calendar import monthrange
from django.contrib.auth import authenticate, login, logout

# Create your views here.
class Dashboard(View):
    template_name = "index.html"
    def get(self, request):
        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12,}

        get_month = request.GET.get("month")
        print(get_month)
        roommates_exp = ExpensePaidAmount.objects.all().last()
        roommate = AddRoommate.objects.all().count()
        
        if roommates_exp:
            if get_month is not None:
                given_month_year = get_month+" "+str(date.today().year)
                roommates_expense = ExpensePaidAmount.objects.filter(month_year=given_month_year)    
                p = PUBBillAmount.objects.filter(food_date=given_month_year)
                roommates_exp = given_month_year
                
                individual = roommates_expense.first()

                if roommate != 0:
                    pub_amt = p.first().total_amt/roommate if p else 0
                    last_month_expense = AddExpenses.objects.filter(date__year=str(date.today().year)).filter(date__month=months.get(get_month)).aggregate(Sum("item_price"))["item_price__sum"]
                    index_pub_total = p.first().total_amt if p else 0

                    if p:
                        for r in roommates_expense:
                            r.pub = float(pub_amt)
                            r.total_paid_pub = r.food_expense + float(pub_amt)
                            r.save()
                    else:
                        for r in roommates_expense:
                            r.total_paid_pub = r.food_expense
                            r.save()

                    group_individual = AddExpenses.objects.filter(date__year=str(date.today().year)).filter(date__month=months.get(get_month)).values("name").annotate(Sum("item_price"))
                    print(group_individual)
                    
                    if roommates_expense and group_individual:
                        for chk_bal in roommates_expense:
                            for gi in group_individual:
                                if str(chk_bal.name).split()[-1][1:-1] == str(gi.get("name")):
                                    total = chk_bal.total_paid_pub if chk_bal.total_paid_pub else 0 
                                    chk_bal.purchase = gi.get("item_price__sum")
                                    chk_bal.save()
                                    chk_bal.balance = total - gi.get("item_price__sum")
                                    chk_bal.save()
                                    print("IF", gi, chk_bal.name, chk_bal.name.name, total, total - gi.get("item_price__sum"))
                                else:
                                    total = chk_bal.total_paid_pub if chk_bal.total_paid_pub else 0
                                    cb_p = chk_bal.purchase
                                    if not cb_p:
                                        chk_bal.balance = total
                                        chk_bal.save()
                                        print("ELSE", total, cb_p)

            else:
                roommates_expense = ExpensePaidAmount.objects.filter(month_year=roommates_exp.month_year)    
                p = PUBBillAmount.objects.filter(food_date=roommates_exp.month_year)
                roommates_exp = roommates_exp.month_year
                individual = roommates_expense.first()

                if roommate != 0:
                    pub_amt = p.first().total_amt/roommate if p else 0
                    last_month_expense = AddExpenses.objects.filter(date__year=roommates_exp.split()[1]).filter(date__month=months.get(roommates_exp.split()[0])).aggregate(Sum("item_price"))["item_price__sum"]
                    index_pub_total = p.first().total_amt if p else 0
                    
                    if p:
                        for r in roommates_expense:
                            r.pub = pub_amt
                            r.total_paid_pub = r.food_expense + pub_amt
                            r.save()
                    else:
                        for r in roommates_expense:
                            r.total_paid_pub = r.food_expense
                            r.save()

                    group_individual = AddExpenses.objects.filter(date__year=roommates_exp.split()[1]).filter(date__month=months.get(roommates_exp.split()[0])).values("name").annotate(Sum("item_price"))
                    
                    if roommates_expense and group_individual:
                        for chk_bal in roommates_expense:
                            for gi in [ i for i in group_individual ]:
                                if str(chk_bal.name).split()[-1][1:-1] == str(gi.get("name")):
                                    total = chk_bal.total_paid_pub if chk_bal.total_paid_pub else 0 
                                    chk_bal.purchase = gi.get("item_price__sum")
                                    chk_bal.save()
                                    chk_bal.balance = total - gi.get("item_price__sum")
                                    chk_bal.save()
                                    print("IF", chk_bal.name, chk_bal.name.name, total, total - gi.get("item_price__sum"))
                                else:
                                    total = chk_bal.total_paid_pub if chk_bal.total_paid_pub else 0
                                    cb_p = chk_bal.purchase
                                    if not cb_p:
                                        chk_bal.balance = total
                                        chk_bal.save()
                                        print("ELSE", total, cb_p)
            
        else:
            roommates_expense = ""
            pub_amt = 0
            if roommate == 0:
                roommate = 0
            last_month_expense = 0
            index_pub_total = 0
            individual = ""
            
        context = {
            "months": months,
            "datas": roommates_expense,
            "last_date": roommates_exp,
            "pub_amt": pub_amt,
            "roommate": roommate,
            "last_month_expense": last_month_expense,
            "index_pub_total": index_pub_total,
            "individual": individual,
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
        months = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6, "July": 7, "August": 8,
                        "September": 9, "October": 10, "November": 11, "December": 12,}
        
        year = date.today().year
        get_month = request.GET.get("month")

        if get_month is None:
            expenses = AddExpenses.objects.filter(date__year=date.today().year).filter(date__month=date.today().month)
            this_month_expense = AddExpenses.objects.filter(date__month=date.today().month).filter(date__year=year).aggregate(Sum("item_price"))["item_price__sum"]
            x = round(this_month_expense, 2) if this_month_expense is not None else this_month_expense
        else:
            expenses = AddExpenses.objects.filter(date__year=year).filter(date__month=months.get(get_month))
            this_month_expense = AddExpenses.objects.filter(date__month=months.get(get_month)).filter(date__year=year).aggregate(Sum("item_price"))["item_price__sum"]
            x = round(this_month_expense, 2) if this_month_expense is not None else this_month_expense
        
        context = {
            "datas": roommates,
            "expenses": expenses,
            "this_month_expense": x,
            "months": months,
            "year": year,
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
            messages.info(request, "PUB Bill Added - {}".format(month_year))

        context = {
            "pubbill": pubbill,
            "months": months,
            "year": date.today().year
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request):
        pre_date = request.POST.get("pre_date")
        prev_read = request.POST.get("prev_read")
        cur_date = request.POST.get("cur_date")
        cur_read = request.POST.get("cur_read")
        removal_amt = request.POST.get("removal_amt")
        water_amt = request.POST.get("water_amt")
        gst = request.POST.get("gst")
        total_units = abs(float(prev_read) - float(cur_read))

        print(pre_date, prev_read, cur_date, cur_read, total_units, removal_amt, water_amt, gst)
        total = (float(total_units) * 0.1495) + float(removal_amt) + float(water_amt)
        add_gst = (total * 7)/100
        total = total + add_gst
        
        bill = PUBBillAmount(pre_date=pre_date, prev_read=prev_read, cur_date=cur_date, cur_read=cur_read, total_units=total_units,
                             refuse_amt=removal_amt, water_amt=water_amt, gst=gst, total_amt=total)
        bill.save()
        return redirect("/pub-bill")

class PubBillEdit(View):
    template_name = "pub_bill.html"
    def get(self, request, pk):
        get_bill = PUBBillAmount.objects.get(id=pk)
        prev_date = get_bill.pre_date.strftime('%Y-%m-%d') #Date Formate - 2020-04-03
        cur_date = get_bill.cur_date.strftime('%Y-%m-%d') #Date Formate - 2020-04-03
        context = {
            "get_bill": get_bill,
            "prev_date": prev_date,
            "cur_date": cur_date,
        }
        return render(request, template_name=self.template_name, context=context)
    
    def post(self, request, pk):
        pre_date = request.POST.get("pre_date")
        prev_read = request.POST.get("prev_read")
        cur_date = request.POST.get("cur_date")
        cur_read = request.POST.get("cur_read")
        removal_amt = request.POST.get("removal_amt")
        water_amt = request.POST.get("water_amt")
        gst = request.POST.get("gst")
        total_units = abs(float(prev_read) - float(cur_read))

        get_bill = PUBBillAmount.objects.get(id=pk)
        get_bill.pre_date = pre_date
        get_bill.prev_read = prev_read
        get_bill.cur_date = cur_date
        get_bill.cur_read = cur_read
        get_bill.removal_amt = removal_amt
        get_bill.water_amt = water_amt
        get_bill.gst = gst
        get_bill.total_units = total_units

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

def roommate_login(request):
    return render(request, template_name="login.html")

def login_auth(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/dashboard")
        else:
            data = {"error": "Username [or] Password Incorrect"}
            return render(request, "login.html", context=data)

def roommate_logout(request):
    logout(request)
    return redirect("/")
