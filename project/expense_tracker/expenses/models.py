from django.db import models
from django.contrib.auth.models import User  
from django.core.validators import MaxValueValidator

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transportation', 'Transportation'),
        ('bills', 'Bills'),
        ('housing', 'Housing'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('others', 'Others'),
    ]

    title = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=12,  # Allows up to 9999999999.99
        decimal_places=2,
        validators=[MaxValueValidator(10000000)],
    )
    category = models.CharField(max_length=100,choices=CATEGORY_CHOICES,)
    description = models.TextField()
    date = models.DateField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    
    def __str__(self):
        return f"{self.title} - {self.amount}"
