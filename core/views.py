from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import User, Profile

global PROFILE_FIELDS
PROFILE_FIELDS = {
        "background": {
            "height_ft": "None",
            "height_in": "None",
            "age": "None",
            "weight": "None", 
            "sex": "None",
            "smoker": "None",
            "alcohol": "None",
        },
        "family_history": {
            "heart_disease": "None",
            "cancer": "None",
        },
        "general": {
            "high_blood_pressure": "None",
            "arrythmia": "None",
            "heart_disease": "None",
        }  
    }

@login_required(redirect_field_name=None)
def index(request):
    return render(request, "core/home.html")

@login_required(redirect_field_name=None)
def profile_view(request):
    
    profile = request.user.profile.profile
    
    return render(request, "core/profile.html", {
        "profile": profile,
        "page_name": "profile",
        
        # Fields for user profile info
        "boolean_fields": ["None", "Yes", "No"],
        "sex_fields": ["None", "Male", "Female"],
        "age_fields": ["None"] + [str(i) for i in range(16,100)],
        "foot_fields": ["None"] + [str(i)+" ft" for i in range(1,8)],
        "inch_fields": ["None"] + [str(i)+" in" for i in range(12)],
        "pound_fields": ["None"] + [str(i)+" lb" for i in range(65, 450)],
        "alcohol_fields": ["None", "Light", "Medium", "Heavy"]
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "core/login.html", {
                "error": "Invalid email and/or password."
            })
    else:
        return render(request, "core/login.html")

def register_view(request):
    if request.method == "POST":
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "core/register.html", {
                "error": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.save()
            
            profile = Profile(user=user, profile=PROFILE_FIELDS)
            profile.save()
        except IntegrityError as e:
            print(e)
            return render(request, "core/register.html", {
                "error": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "core/register.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
