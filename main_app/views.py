from django.shortcuts import render, redirect 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from django import forms
from .models import Trip, Member, Transaction
from django.urls import reverse
import locale
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


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

@login_required
def user_trips(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'main_app/user_detail.html', {'trips' : trips})

class TripCreate(LoginRequiredMixin, CreateView):
    model = Trip
    fields = ['name', 'start_date', 'end_date']

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        member = Member(trip = self.object, name = self.request.user.first_name)
        member.total = 0
        member.save()
        return response
    
    def get_success_url(self):
        return reverse('trip_detail', kwargs={'pk': self.object.pk})
    
class TripDetail(LoginRequiredMixin, DetailView):
    model = Trip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = self.get_object()
        transactions = Transaction.objects.filter(trip=trip)
        members = Member.objects.filter(trip=trip)

        locale.setlocale(locale.LC_ALL, '')
        total_spent = sum(transaction.amount for transaction in transactions)
        formatted_total_spent = locale.currency(total_spent, grouping=True)

        for transaction in transactions:
            individual_amt = transaction.individual_amt
            formatted_individual_amt = locale.currency(individual_amt, grouping=True)
            transaction.formatted_individual_amt = formatted_individual_amt

        context['trip'] = self.object
        context['members'] = members
        context['transactions'] = transactions
        context['total_spent'] = formatted_total_spent
        return context

class TripUpdate(LoginRequiredMixin, UpdateView):
    model = Trip
    fields = ['name', 'start_date', 'end_date']
    template_name = 'main_app/trip_edit_form.html'

    def get_success_url(self):
        return reverse('trip_detail', kwargs={'pk': self.kwargs['pk']})

class TripDelete(LoginRequiredMixin, DeleteView):
    model = Trip
    fields = '__all__'
    success_url = '/trips'

class MemberCreate(LoginRequiredMixin, CreateView):
    model = Member
    fields = ['name']
    template_name = 'main_app/member_form.html'

    def form_valid(self, form):
        trip = Trip.objects.get(id = self.kwargs['pk'])
        form.instance.trip = trip
        form.instance.total = 0
        return super().form_valid(form)
   
    def get_success_url(self):
        return reverse('trip_detail', kwargs={'pk': self.kwargs['pk']})


class MemberUpdate(LoginRequiredMixin, UpdateView):
    model = Member
    fields = ['name']
    template_name = 'main_app/member_edit_form.html'

    def get_success_url(self):
        trip_id = self.kwargs['trip_id']
        return reverse('trip_detail', kwargs={'pk': trip_id})


class MemberDelete(LoginRequiredMixin, DeleteView):
    model = Member
    fields = '__all__'

    def get_success_url(self):
        trip_id = self.kwargs['trip_id']
        return reverse('trip_detail', kwargs={'pk': trip_id})
    
class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['name', 'description', 'amount', 'date', 'paid_by', 'paid_for']
    template_name = 'main_app/transaction_form.html'


    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        trip = Trip.objects.get(pk=self.kwargs['pk'])
        members = Member.objects.filter(trip=trip)
        member_choices = [(member.pk, member.name) for member in members]
        form.fields['paid_by'].choices = member_choices
        form.fields['paid_for'].choices = member_choices
        return form


    def form_valid(self, form):
        form.instance.trip = Trip.objects.get(pk=self.kwargs['pk'])
        paid_by = form.cleaned_data['paid_by']
        paid_by.total += form.cleaned_data['amount']
        paid_by.save()

        amount = form.cleaned_data['amount']
        members = form.cleaned_data['paid_for']
        num_members = len(members)
        individual_amt = amount / num_members

        transaction = form.save(commit=False)
        transaction.individual_amt = individual_amt
        transaction.save()
        transaction.paid_for.set(members)

        return super().form_valid(form)
    
    def get_success_url(self):
        trip_id = self.kwargs['pk']
        return reverse('trip_detail', kwargs={'pk': trip_id})

class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['name', 'description', 'amount', 'date', 'paid_by', 'paid_for']
    template_name = 'main_app/transaction_edit_form.html'

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        trip = Trip.objects.get(pk=self.kwargs['trip_id'])
        members = Member.objects.filter(trip=trip)
        member_choices = [(member.pk, member.name) for member in members]
        form.fields['paid_by'].choices = member_choices
        form.fields['paid_for'].choices = member_choices
        return form
    
    def form_valid(self, form):
        paid_by = form.cleaned_data['paid_by']
        paid_by.total += form.cleaned_data['amount']
        paid_by.save()

        amount = form.cleaned_data['amount']
        members = form.cleaned_data['paid_for']
        num_members = len(members)
        individual_amt = amount / num_members

        transaction = form.save(commit=False)
        transaction.individual_amt = individual_amt
        transaction.save()
        transaction.paid_for.set(members)

        return super().form_valid(form)
    
    def get_success_url(self):
        trip_id = self.kwargs['trip_id']
        return reverse('trip_detail', kwargs={'pk': trip_id})

class TransactionDelete(LoginRequiredMixin, DeleteView):
    model = Transaction
    fields = '__all__'

    def get_success_url(self):
        trip_id = self.kwargs['trip_id']
        return reverse('trip_detail', kwargs={'pk': trip_id})