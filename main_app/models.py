from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Trip(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    
class Member(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    name = models.CharField()
    total = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField()
    paid_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='transaction_paid_by')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    paid_for = models.ManyToManyField(Member)
    individual_amt = models.DecimalField(max_digits=8, decimal_places=2)

