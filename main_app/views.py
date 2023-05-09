from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.forms.forms import Form
from django import forms
from .models import User, Trip, Member, Transaction

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30)    
    email = forms.EmailField(label='Email',required=True)  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
       

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  form = CustomUserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def user_trips(request):
   trips = Trip.objects.filter(user=request.user)
   return render(request, 'main_app/user_detail.html', {
      'trips' : trips
   })

class TripCreate(CreateView):
    model = Trip
    fields = ['name', 'start_date', 'end_date']
    success_url = '/trips'

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        member = Member(trip = self.object, name = self.request.user.first_name)
        member.save()
        return response
