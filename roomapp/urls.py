"""roomapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from room import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.Dashboard.as_view()),
    path("addroomate", views.AddRoomies.as_view()),
    path("addroomate-edit/<int:pk>", views.AddRoomiesEdit.as_view()),
    path("addroomate/<int:pk>", views.AddRoomiesDelete.as_view()),
    path("add-expense", views.AddExpense.as_view()), 
    path("add-expense-edit/<int:pk>", views.AddExpenseEdit.as_view()),
    path("add-expense/<int:pk>", views.AddExpenseDelete.as_view()),
    path("calculate-expense", views.CalculteExpense.as_view()),
    path("pub-bill", views.PubBill.as_view()),
    path("pub-edit/<int:pk>", views.PubBillEdit.as_view()), 
    path("pub-delete/<int:pk>", views.PubBillDelete.as_view()),
]
