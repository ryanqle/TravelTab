from django.contrib import admin
from .models import Trip, Member, Transaction

# Register your models here.
admin.site.register(Trip)
admin.site.register(Member)
admin.site.register(Transaction)