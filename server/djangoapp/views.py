from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from djangoapp import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)
# ...


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)
# Create a `login_request` view to handle sign in request
# def login_request(request):
def login_request(request):
    context = {}
    if request.method == "POST":
        username,password = request.POST['username'], request.POST['psw']
        user = authenticate(username=username, password=password) 
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
def logout_request(request):
    context = {}
    print("log out the user `{}`".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html', context)

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
def registration_request(request):
    context = {}
    # rend if it is a GET req
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # get user info
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
            # create new user
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership"
        # Get dealers from the URL
        context = {
            "dealerships": get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url_r = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review?dealerId={dealer_id}"
        url_ds = f"https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/dealership?dealerId={dealer_id}"
        # Get dealers from the URL
        context = {
            "dealer": get_dealers_from_cf(url_ds)[0],
            "reviews": get_dealer_reviews_from_cf(url_r, dealer_id),
        }
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):

    if request.user.is_authenticated:
        context={}
        if request.method == "GET":
            cars = models.CarModel.objects.filter(dealer_id=dealer_id)
            #cars = models.CarModel.objects.filter(dealer_id=dealer_id)
            context['cars'] = cars
            context['dealer_id']=dealer_id
            return render(request, 'djangoapp/add_review.html', context)
        elif request.method == "POST":
            print(request.POST)
            url = "https://service.eu.apiconnect.ibmcloud.com/gws/apigateway/api/a9220b6d6b26f1eb3b657a98770b743616f7d4cd223b89cd1ca4e88ab49bdb92/api/review"
            review = {}
            #review["id"] = get_reviews_count(url) + '{#}'
            review["id"] = get_reviews_count(url) + 1
            review["time"] = datetime.utcnow().isoformat()
            review["dealerId"] = dealer_id
            review["review"] = request.POST["content"]
            review["name"] = request.user.username
            if request.POST['purchasecheck'] == "on":
                review["purchase"] = True #change from True
            else:
                review["purchase"] = False
                review["purchase_date"]= request.POST["purchasedate"]
                review["car_make"] = models.carmake.name
                review["car_model"] = models.carmodel.name
                review["car_year"]= models.carmodel.year.strftime("%Y")
                #review["car_make"] = car.carmake.name
                #review["car_model"] = car.name
                #review["car_year"]= car.year.strftime("%Y")
                
                #review["car_make"]= "Jeep"
                #review["car_model"]= "Gladiator"
                #review["car_year"]= 2021

                json_payload = {}
                json_payload = review
                print (json_payload)
                #restapis.post_request(url, json_payload, dealerId=dealer_id)
                response = post_request(url, json_payload, params=review)
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        else:
            return HttpResponse("Invalid Request type: " + request.method)
    else:
        return HttpResponse("User not authenticated")