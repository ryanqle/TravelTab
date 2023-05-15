<div align="center">

<img src="https://imgur.com/a/PZDT3cv">

# TravelTab

### Built by: **[Ryan Q Le](https://www.linkedin.com/in/ryanqle/)**


[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
![Maintainer](https://img.shields.io/badge/Maintainer-ryanqle-blue)
![Ask](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)

![Django](https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![CSS](https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)


![Git](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)

![Heroku badge](https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white)


## **[CLICK HERE](https://traveltab.herokuapp.com/)**
</div>


## About

Say goodbye to confusion and disputes about who paid for what - **TravelTab** makes it easy to record and split expenses among your travel group. With **TravelTab**, you can create a trip, add your travel companions, and start adding expenses. The app automatically calculates the total cost and who owes what, making it simple to settle expenses at the end of your trip. Whether you're backpacking through Europe or planning a weekend getaway with friends, **TravelTab** is the perfect app to help you keep track of your expenses and stay organized on your travels.

## Getting Started

<img src="https://imgur.com/GXWeMu5">

Once a user signs up and log in. They can view their trips in the **My Trips** tab. **My Trips** will display all of their trip logs. Inside the trip view, users will be able to **Add Members** and **Add Transactions** to the tracker.

**Add Transaction** will display a form for the Name of the transaction, an optional description memo field, amount, date of transaction, paid by and paid for selection of members on the trip.

<div align="center">

![Gif](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMGUxOTlkNTRhYjE4YjRiNmI4ZjE5YmY4ZDM2NjY3MzczMmQzOTY5ZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/4f4t2yd4zX7yJZnweP/giphy.gif)
</div>

## Interesting Code

From the views.py, the logic of evenly split costs

```python
class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['name', 'description', 'amount', 'date', 'paid_by', 'paid_for']
    template_name = 'main_app/transaction_form.html'

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
```

## Future Plans
- [] Add other users as members where multiple users can make edits to the trip
- [] Split by shares or specific amounts
- [] More responsive design for mobile users


## Associated Links:

**[TRELLO](https://trello.com/b/f6NRqORs/traveltab)**

**[Wireframe](https://whimsical.com/traveltab-XRB3nQdHRLTs2L9mMm9q3K)**
**[ERD](https://whimsical.com/traveltab-G3yY8CmfwDdALb1ZRiiujJ)**
