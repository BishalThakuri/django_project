from django import forms
from .models import Expense
from django.core.exceptions import ValidationError
from datetime import date
from django.core.validators import MaxValueValidator
from decimal import Decimal, ROUND_DOWN


class ExpenseSearchForm(forms.Form):
    title = forms.CharField(
            max_length=100,
            widget=forms.TextInput(attrs={'placeholder': 'Enter title'}),
            required=True
        )

W

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'description', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),  # Allows decimals
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Add a brief description (optional)'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'title': {
                'required': "Title is required.",
            },
            'amount': {
                'required': "Amount is required.",
            },
            'date': {
                'required': "Please provide a valid date.",
            },
        }


    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be a positive number.")
        if amount > 10000000:
            raise forms.ValidationError("Amount cannot exceed Rs 10,000,000.")
        return amount


    def clean_title(self):
        title = self.cleaned_data.get('title')
        errors = []
        if title.isdigit():
            errors.append("Title should not be a number.")
        if len(title) > 100:
            errors.append("Title should not exceed 100 characters.")
        if errors:
            raise forms.ValidationError(errors)
        return title

    def clean_date(self):
        expense_date = self.cleaned_data.get('date')
        if not expense_date:
            raise forms.ValidationError("Date is required.")
        if expense_date > date.today():
            raise forms.ValidationError("Date cannot be in the future.")
        return expense_date

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            raise forms.ValidationError("Please select a category.")
        
        # Get categories from the model field choices
        valid_categories = dict(Expense.CATEGORY_CHOICES).keys()  # Assuming CATEGORY_CHOICES is a tuple of (value, label)
        if category not in valid_categories:
            raise forms.ValidationError("Invalid category selected.")
        return category


    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            return ""  # Return an empty string for no description
        return description

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        category = cleaned_data.get('category')

        if amount and category == 'Entertainment' and amount > 1000:
            raise forms.ValidationError("Entertainment expenses cannot exceed $1000.")

        return cleaned_data
