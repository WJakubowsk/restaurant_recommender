from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful sign-up
            return redirect("home")  # Redirect to the homepage or another page
    else:
        form = UserCreationForm()
    return render(request, "authentication/signup.html", {"form": form})
