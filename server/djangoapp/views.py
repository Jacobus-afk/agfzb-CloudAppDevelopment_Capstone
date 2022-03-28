from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from djangoapp.models import CarModel

from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

    


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method != "POST":
        return redirect('djangoapp:index')


    username = request.POST.get('username')
    password = request.POST.get('psw')
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('djangoapp:index')
    else:
        messages.warning(request, "Invalid username or password.")
        return redirect('djangoapp:index')

        
# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    # if request.method == 'GET':
    #     return render(request, 'djangoapp/registration.html')
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "User already exists.")
            return render(request, 'djangoapp/registration.html')
    return render(request, 'djangoapp/registration.html')
# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

def get_dealerships(request):
    if request.method != "GET":
        return redirect('djangoapp:index')

    context = {}
    # Get dealers from the URL
    dealerships = get_dealers_from_cf()
    context['dealership_list'] = dealerships
    context['dealership_table'] = {
        'id': 'ID',
        'full_name': 'Dealer Name',
        'city': 'City',
        'address': 'Address',
        'zip': 'Zip',
        'st': 'State',
    }
    # Concat all dealer's short name
    # for dealer in dealerships:
    #     print(dealer["full_name"])
    # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

    return render(request, 'djangoapp/index.html', context)
        # Return a list of dealer short name
        # return HttpResponse(dealer_names)
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...



def get_dealer_details(request, dealer_id):
    if request.method != "GET":
        return redirect('djangoapp:index')

    dealership = get_dealers_from_cf(dealer_id)

    
    dealer_reviews = get_dealer_reviews_from_cf(dealer_id)
    context = {
        'review_list': dealer_reviews,
        'dealer_id': dealer_id,
        'dealer_name': dealership["full_name"]
    }

    # review_list = []
    # # reviews = ' '.join([review.review for review in dealer_reviews])
    # for review in dealer_reviews:
    #     review_list.append(f"{review}<br>")
    return render(request, 'djangoapp/dealer_details.html', context)
        # return HttpResponse(review_list)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    if not request.user.is_authenticated:
        return redirect("djangoapp:index")
    
    url = "https://399ca718.eu-gb.apigw.appdomain.cloud/api/review"
    context = {}
    # json_payload = {}

    # json_payload['review'] = {
    #     'time': datetime.utcnow().isoformat(),
    #     'name': request.user.username,
    #     'dealership': dealer_id,
    #     'review': "This capstone project sucks.. It needs to be proofread.. I'm not a mindreader, I don't know how the lecturer intends for the parts to work together. Not a great motivator for using IBM cloud after this course is completed tbh.."
    # }

    if request.method == 'POST':

        json_payload['review'] = {
            'time': datetime.utcnow().isoformat(),
            'name': request.user.username,
            'dealership': dealer_id,
            'car_year': car.year.strftime("%Y")
        #     'review': "This capstone project sucks.. It needs to be proofread.. I'm not a mindreader, I don't know how the lecturer intends for the parts to work together. Not a great motivator for using IBM cloud after this course is completed tbh.."
        }

        resp = post_request(url, json_payload)

        return HttpResponse(resp)

    cars = CarModel.objects.filter(dealer_id=dealer_id)
    dealership = get_dealers_from_cf(dealer_id)


    context['cars'] = cars
    context['dealer_id'] = dealer_id
    context['dealer_name'] = dea

    return render(request, 'djangoapp/add_review.html', context)