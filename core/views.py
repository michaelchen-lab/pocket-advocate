from datetime import datetime
from collections import OrderedDict

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .models import User, Profile, Symptom, SymptomRecord
from .utils import get_recommendation

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

def is_date_valid(DD, MM, YY):
    try:
        dt = datetime(int(YY), int(MM), int(DD))
        return True
    except:
        return False

@login_required(redirect_field_name=None)
def index(request):
    if request.method == "POST":
        symptom = request.POST["symptom"]
        DD, MM, YY = request.POST["DD"], request.POST["MM"], request.POST["YY"]
        score = request.POST["score"]
        
        print(DD, MM, YY)
        
        if symptom == "Your Symptom..." or DD == "DD" or MM == "MM" or YY == "YY":
            print('error')
        elif not is_date_valid(DD, MM, YY):
            print('error')
        else:
            record = SymptomRecord(
                user = request.user, 
                symptom = Symptom.objects.get(title=symptom),
                date = YY+"-"+MM+"-"+DD,
                score = int(score)
            )
            record.save()
    
    records = list(request.user.SymptomRecords.order_by('symptom_id', 'date').values('symptom_id', 'date', 'score'))
    symptom_ids = list(set([record['symptom_id'] for record in records]))
    my_symptoms = {Symptom.objects.get(id=id).title:id for id in symptom_ids}
    
    background = request.user.profile.profile['background']
    background['height'] = background['height_ft'] + ' ' + background['height_in']
    
    recommendations = request.user.profile.recommendations
    recommendations = dict(OrderedDict(reversed(list(OrderedDict(recommendations).items()))))
    if recommendations != {}:
        for diagnosis,details in recommendations.items():
            my_diagnosis = diagnosis
            my_medications = [detail['Medication'] for detail in details]
            my_medications = [my_medications[i:i+2] for i in range(0, len(my_medications), 2)] 
            break
    else:
        my_diagnosis = False
        my_medications = False
    
    symptoms = [symptom.title if len(symptom.title) < 70 else symptom.title[:70]+'...' for symptom in Symptom.objects.all()]

    return render(request, "core/home.html", {
        "symptoms_input": ['Your Symptom...']+symptoms,
        "dates_input": ['DD']+[str(d) if len(str(d)) == 2 else '0'+str(d) for d in range(1,32)],
        "months_input": ['MM']+[str(d) if len(str(d)) == 2 else '0'+str(d) for d in range(1,13)],
        "years_input": ['YY']+list(range(2016, 2021)),
        
        "my_symptoms": my_symptoms,
        "records": records,
        "background": background,
        "my_diagnosis": my_diagnosis,
        "my_medications": my_medications
    })

@login_required(redirect_field_name=None)
def recommendation_view(request):
    if request.method == "POST":
        diagnosis = request.POST["diagnosis"]
        data = {} ## Background info, symptom history, diagnosis
        recommendation_data = get_recommendation(data)
        print(recommendation_data)
        
        request.user.profile.recommendations[diagnosis] = recommendation_data
        print(request.user.profile.recommendations)
        request.user.profile.save()
        
    recommendations = request.user.profile.recommendations
    return render(request, "core/recommendation.html", {
        "page_name": "recommend",
        "recommendations": dict(OrderedDict(reversed(list(OrderedDict(recommendations).items()))))
    })

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
            
            profile = Profile(
                user=user, 
                profile=PROFILE_FIELDS,
                recommendations=[]
            )
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
