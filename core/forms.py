from django import forms
from .models import Project, Client, Invoice, Payment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'client', 'start_date', 'end_date', 'value', 'status', 'image', 'observations']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone', 'contact_number', 'image']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['project', 'due_date', 'total_amount', 'status']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['invoice', 'amount']
