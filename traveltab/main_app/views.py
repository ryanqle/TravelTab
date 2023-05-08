from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.forms.forms import Form
from django import forms  

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150, required=True)  
    email = forms.EmailField(label='Email',required=True)  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.') 

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