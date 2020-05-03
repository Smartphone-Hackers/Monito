from django import forms
from room.models import AddRoommate

class AddRoommateForm(forms.Form):
    class Meta:
        model = AddRoommate
        fields = ["name", "phone"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter Name"}),
            "phone": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter Phone Number"}),
        }