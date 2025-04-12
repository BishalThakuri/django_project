from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Expense
from .forms import ExpenseForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .utils import validate_expense
from .forms import ExpenseSearchForm

# Home view

@login_required
def home(request):
    form = ExpenseSearchForm(request.GET)
    expenses = Expense.objects.filter(user=request.user)
    if form.is_valid():
        title = form.cleaned_data.get('title')
        if title:
            expenses = expenses.filter(title__icontains=title)

    # Aggregated data for chart or summary
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    category_data = expenses.values('category').annotate(total_amount=Sum('amount'))
    categories = [item['category'] for item in category_data]
    amounts = [float(item['total_amount']) for item in category_data]
    
    first_date = expenses.order_by('date').first().date if expenses.exists() else None
    last_date = expenses.order_by('-date').first().date if expenses.exists() else None

    return render(request, 'home.html', {
        'expenses': expenses,
        'form': form,
        'categories': categories,
        'amounts': amounts,
        'total_amount': total_amount,
        'first_date': first_date,
        'last_date': last_date,
    })


# Add Items
@login_required
def add_items(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user  # Assign current user

            # Custom validation for amount
            if expense.amount > 10000000:
                messages.error(request, "Amount cannot exceed Rs 10,000,000.")
                return redirect('add_items')

            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")

    else:
        form = ExpenseForm()

    return render(request, 'add.html', {'form': form})



# Delete an expense
@login_required
def delete_item(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('home')


# Login Section
def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome , {user.username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Logout Section
def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')


# Register Page
def register_page(request):
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'register.html', {'form': form})


# Edit Item

@login_required
def edit_item(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)

            # Use the validation function
            error = validate_expense(expense)
            if error:
                messages.error(request, error)
                return redirect('edit_item', id=id)

            expense.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'edit_expense.html', {'form': form, 'expense': expense})


