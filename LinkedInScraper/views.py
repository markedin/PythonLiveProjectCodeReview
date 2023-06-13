from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from .models import User
import requests
from bs4 import BeautifulSoup
import json


# Creating basic app
def lis_home(request):
    return render(request, 'LinkedInScraper/lis_home.html')


# this function will render the create new user page when requested

def create_user(request):
    form = UserForm(data=request.POST or None)  # retrieve user form
    # checks if req method is POST
    if request.method == 'POST':
        if form.is_valid():  # check to see if the submitted form is valid and if so, saves the form
            form.save()  # saves new acc
            return redirect('lis_home')  # returns user back to the home page
    content = {'form': form}  # saves content to the template as a dictionary
    # adds content of form to page
    return render(request, 'LinkedInScraper/CreateUser_lis.html', content)


# this function will render the list users page when requested

def list_users(request):
    users = User.Users.all()
    content = {'users': users}
    return render(request, 'LinkedInScraper/ListUsers_lis.html', content)


def details(request, pk):
    pk = int(pk)
    user = get_object_or_404(User, pk=pk)
    form = UserForm(data=request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.save()
            return redirect('lis_home')
        else:
            print(form.errors)
    else:
        return render(request, 'LinkedInScraper/Details_lis.html', {'form': form})
    content = {'user': user}
    return render(request, 'LinkedInScraper/Details_lis.html', content)


def delete(request, pk):
    pk = int(pk)
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('lis_home')
    content = {'user': user}
    return render(request, 'LinkedInScraper/ConfirmDelete.html', content)


def bs4_practice(request):
    if request.method == "POST":
        url = request.POST.get('url')  # get url from input
        req = requests.get(url)  # make the request
        web_s = req.text  # get the content of the request
        soup = BeautifulSoup(web_s, "html.parser")  # parse it
        title = soup.title.string  # get the value of the title tag of inputted page
        atags = soup.find_all('a')
        ptags = soup.find_all('p')
        alltext = soup.get_text()

        context = {'title': title, 'atags': atags, 'ptags': ptags, 'alltext': alltext}
        return render(request, 'LinkedInScraper/BS4_practice.html', context)

    return render(request, "LinkedInScraper/BS4_practice.html")




def save_api_data(jsonObj):
    results = jsonObj["results"]
    newDict = results
    for user in newDict:
        if User.Users.filter(profile_id=user['profile_id']).exists():
            continue
        u = User()        
        u.first_name = user["first_name"]
        u.profile_id = user["profile_id"]
        u.position = user["sub_title"]
        u.location = user["location"]["short"]
        u.industry = user["industry"]
        u.last_name = user["last_name"]
        u.save()




def ScraperAPI(request):
    with open('./LinkedInScraper/apiresults.json') as r:
        response = json.load(r)
        save_api_data(response)
        db_results = User.Users.all()
        context = {'results': db_results}

        return render(request, "LinkedInScraper/ScraperAPI.html", context)


def show_favoriteUsers(request):
    return render(request, "LinkedInScraper/show_favoriteUsers.html")


def getAPIdata(request, position, location):

    if request.method == 'POST':
        url = "https://linkedin-profiles-and-company-data.p.rapidapi.com/linkedin-search"

        payload = {
            "keyword": str(position),
            "search_type": "people",
            "location": str(location),
            "size": "11-50",
            "per_page": 50,
            "offset": 0
        }
        headers = {
            "content-type": "application/json",
            # Removed key and host so I don't incur charges by making all of this code public :) 
            "X-RapidAPI-Key": "KEY",
            "X-RapidAPI-Host": "HOST"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response

