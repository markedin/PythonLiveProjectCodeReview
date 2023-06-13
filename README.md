# Python Live Project

## Introduction
For the last two weeks of my time at the tech academy, I worked with my peers in a team developing a full scale Django application in Python. The project was set up so I would build a Django application that was part of the "AppBuilder9000". The application I decided to build was a "LinkedInScraper" tool. It did not perform the actual web scraping [(turns out scraping linkedin is not advised)](https://www.getmagical.com/blog/linkedin-data-scraping). I only had 2 weeks to work on my project, and I decided to use an API rather than creating a bunch of fake bot accounts to scrape with. Unfortunately, 2 days before my project ended, the API I was using removed the "user search" endpoint. For the sake of demonstrating how my project works, I will be reading from a .json file I saved that is exactly what the API results look like.

 Unlike the C# live project, I did not spend any time fixing bugs, but instead used my time developing an application by completing user stories. I worked on mostly [back end stories](#back-end-stories), but also a good amount of [front end stories](#front-end-stories) and UX improvements. I also had the chance to work with some instructors to improve my development [skills](#other-skills-learned). 

Below are descriptions of the stories I worked on, along with code snippets and navigation links. I also have some full code files in this repo for the larger functionalities I implemented.

## Back End Stories
* [User Model](#user-model)
* [CRUD Functionality](#crud-functionality)
* [Beutiful Soup Practice](#bs4-practice)
* [API Integration](#api-integration)

### User Model
This model contains all of the important information that I wanted to save when searching for a linked in profile. Not all the fields are filled when API results are returned, but they provide a placeholder incase I recieve that information at a later time. The FavoritedUser model comes in handy later when I create a "favorites" list. 
```python
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    phone_num = models.CharField(max_length=15)
    email_addr = models.CharField(max_length=30)
    profile_id = models.CharField(max_length=100)
    company = models.CharField(max_length=30)
    industry = models.CharField(max_length=50, null=True)
    position = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)

    # defines the model manager for users
    Users = models.Manager()


class FavoritedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    FavoritedUsers = models.Manager()

```
### CRUD Functionality
These methods allow CRUD functionality regarding stored users. I was surprised to see how easy this task is when using Django to build projects. The details method provides the read/update functionality, since I am able to edit the forms inputs and then save them using a button contained in the template. 

```py
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
```

### BS4 Practice

This method was some quick practice using the Beautiful Soup webscraping module. It provided the functionality to pull all of the "a-tags", "p-tags" and all text that was present on a webpage when you enter in a URL. I wish I had more time to explore the many use cases of this module. I will definitely be doing some personal projects with it in the future. 

```python
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

```


### API Integration
This is where I spent most of my time during the live project. The first thing I did was try and call the API to return linked in search results. This is what my "API calling function" looked like. 

```py
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
            "X-RapidAPI-Key": "KEY",
            "X-RapidAPI-Host": "HOST"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response
```

This function was called in my ScraperAPI method that was called every time I opened the page. This was going to be changed to call the API and pass in the "position" and "location" parameters with a button press, but I ran out of time because of the API endpoint deletion. 

Because the endpoint was deleted, I had to read the "API Results" from a .json file that was an exact copy of what the API returned. Because I only had 100 free API calls per month, this actually saved me a ton of calls because I could just read from this file while debugging. 

<details>
    <summary>Click here to see the JSON file</summary>

```json

{
  "info": "For high-volume use of our LinkedIn API, visit https://iscraper.io or send an email at sales@iscraper.io to discuss the pricing.",
  "meta": {
    "page": 1,
    "total": null,
    "per_page": 20,
    "search_type": "people"
  },
  "results": [
    {
      "first_name": "Paul",
      "profile_id": "paul-tremblay-98a1703b",
      "sub_title": "Senior Accounting Professional",
      "location": {
        "short": "El Cajon, California",
        "city": "El Cajon",
        "country": "United States",
        "default": "El Cajon, California, United States",
        "state": "California"
      },
      "industry": "Non-profit Organization Management",
      "profile_picture": null,
      "last_name": "Tremblay"
    },
    {
      "first_name": "Kirchner",
      "profile_id": "kirchner-daniel-478a589",
      "sub_title": "Defined Contributions Analyst at Milliman & Robertson",
      "location": {
        "short": "Albany, New York",
        "city": "Albany",
        "country": "United States",
        "default": "Albany, New York, United States",
        "state": "New York"
      },
      "industry": "Financial Services",
      "profile_picture": null,
      "last_name": "Daniel"
    },
    {
      "first_name": "Nicole",
      "profile_id": "nicole-dawn-2550a8126",
      "sub_title": "Apps Systems Engineer at Insight Global\n",
      "location": {
        "short": "Fort Mill, South Carolina",
        "city": "Fort Mill",
        "country": "United States",
        "default": "Fort Mill, South Carolina, United States",
        "state": "South Carolina"
      },
      "industry": "Financial Services",
      "profile_picture": null,
      "last_name": "Dawn"
    },
    {
      "first_name": "Patrick",
      "profile_id": "patrick-bresnahan-3a59752b",
      "sub_title": "Account Executive at ARAMARK",
      "location": {
        "short": "St Louis, Missouri",
        "city": "St Louis",
        "country": "United States",
        "default": "St Louis, Missouri, United States",
        "state": "Missouri"
      },
      "industry": "Retail",
      "profile_picture": null,
      "last_name": "Bresnahan"
    },
    {
      "first_name": "Elizabeth",
      "profile_id": "elizabeth-berridge-17b45786",
      "sub_title": "University of Washington",
      "location": {
        "short": "Seattle, Washington",
        "city": "Seattle",
        "country": "United States",
        "default": "Seattle, Washington, United States",
        "state": "Washington"
      },
      "industry": "Higher Education",
      "profile_picture": null,
      "last_name": "Berridge"
    },
    {
      "first_name": "Mary",
      "profile_id": "mary-maragos-42730b81",
      "sub_title": "District League Coordinator at USTA Nevada",
      "location": {
        "short": "Las Vegas, Nevada",
        "city": "Las Vegas",
        "country": "United States",
        "default": "Las Vegas, Nevada, United States",
        "state": "Nevada"
      },
      "industry": "Sports",
      "profile_picture": null,
      "last_name": "Maragos"
    },
    {
      "first_name": "Mike",
      "profile_id": "mike-barrera-21b27217",
      "sub_title": "Asst. Supt. District Ops at McAllen ISD",
      "location": {
        "short": "McAllen, Texas",
        "city": "McAllen",
        "country": "United States",
        "default": "McAllen, Texas, United States",
        "state": "Texas"
      },
      "industry": "Education Management",
      "profile_picture": null,
      "last_name": "Barrera"
    },
    {
      "first_name": "R Larry",
      "profile_id": "rlarryatwell",
      "sub_title": "Product Management and Wireless Innovation Executive",
      "location": {
        "short": "Denver, Colorado",
        "city": "Denver",
        "country": "United States",
        "default": "Denver, Colorado, United States",
        "state": "Colorado"
      },
      "industry": "Wireless",
      "profile_picture": null,
      "last_name": "A."
    },
    {
      "first_name": "Kevin",
      "profile_id": "kevin-carmody",
      "sub_title": "Senior Partner at McKinsey & Company",
      "location": {
        "short": "Greater Chicago Area",
        "city": null,
        "country": "United States",
        "default": "Greater Chicago Area",
        "state": null
      },
      "industry": "Management Consulting",
      "profile_picture": "https://media.licdn.com/dms/image/D5603AQHSSxyTWcU91w/profile-displayphoto-shrink_800_800/0/1682872580601?e=1691020800&v=beta&t=jdUfZ02MltnsKu_TempWcLN2-b7gxVPewU4ieOk91DY",
      "last_name": "Carmody"
    },
    {
      "first_name": "Patti",
      "profile_id": "patti-briggs-76b66430",
      "sub_title": "sales specialist & partner at Retirement Dynamics",
      "location": {
        "short": "Charlotte, North Carolina",
        "city": "Charlotte",
        "country": "United States",
        "default": "Charlotte, North Carolina, United States",
        "state": "North Carolina"
      },
      "industry": "Marketing & Advertising",
      "profile_picture": null,
      "last_name": "Briggs"
    },
    {
      "first_name": "Michael",
      "profile_id": "michael-bonventre-b2ab9154",
      "sub_title": "Global Finance Director at TI Fluid Systems",
      "location": {
        "short": "Auburn Hills, Michigan",
        "city": "Auburn Hills",
        "country": "United States",
        "default": "Auburn Hills, Michigan, United States",
        "state": "Michigan"
      },
      "industry": "Automotive",
      "profile_picture": null,
      "last_name": "Bonventre"
    },
    {
      "first_name": "Jason",
      "profile_id": "jason-weiler-076a2b10",
      "sub_title": "Director IT Solutions, Automotive Americas at SYNCREON",
      "location": {
        "short": "London, Ontario",
        "city": "London",
        "country": "Canada",
        "default": "London, Ontario, Canada",
        "state": "Ontario"
      },
      "industry": "Logistics & Supply Chain",
      "profile_picture": "https://media.licdn.com/dms/image/C5603AQH1zYmxG7FKwA/profile-displayphoto-shrink_800_800/0/1517738246313?e=1691625600&v=beta&t=inXR6vNwP6RFp1PfWxuSoc-6KNgfIFgttqmtGojEEBE",
      "last_name": "Weiler"
    },
    {
      "first_name": "Scott",
      "profile_id": "scott-britton-335a5211",
      "sub_title": "Shareholder at Ford & Britton PC",
      "location": {
        "short": "Greater Chicago Area",
        "city": null,
        "country": "United States",
        "default": "Greater Chicago Area",
        "state": null
      },
      "industry": "Law Practice",
      "profile_picture": "https://media.licdn.com/dms/image/C4E03AQFrhXfH6j7zCg/profile-displayphoto-shrink_800_800/0/1546446230414?e=1691625600&v=beta&t=aEArEYtvsqnIrUyTm3GU_6i5WJaulP309BWxER6B-0M",
      "last_name": "Britton"
    },
    {
      "first_name": "Matthew",
      "profile_id": "matthew-garcia-7807a08",
      "sub_title": "Senior Mortgage Loan Officer at Supreme Lending",
      "location": {
        "short": "Atlanta, Georgia",
        "city": "Atlanta",
        "country": "United States",
        "default": "Atlanta, Georgia, United States",
        "state": "Georgia"
      },
      "industry": "Real Estate",
      "profile_picture": "https://media.licdn.com/dms/image/C4E03AQGmxyvzZC2JXQ/profile-displayphoto-shrink_800_800/0/1517733231919?e=1691625600&v=beta&t=B2jWfEGWHlozQqXt4c8pxIdopJIMDwhbDnlmBBSTcW8",
      "last_name": "Garcia"
    },
    {
      "first_name": "Bubba",
      "profile_id": "bubba-bailey-4887301a",
      "sub_title": "Senior Loan Officer at Movement Mortgage",
      "location": {
        "short": "Rock Hill, South Carolina",
        "city": "Rock Hill",
        "country": "United States",
        "default": "Rock Hill, South Carolina, United States",
        "state": "South Carolina"
      },
      "industry": "Banking",
      "profile_picture": "https://media.licdn.com/dms/image/D5603AQHxrRXMEtNewA/profile-displayphoto-shrink_800_800/0/1680787646649?e=1691625600&v=beta&t=Gh7rMvgKOnMFqX73-2zCg_roER1u5NMKhX5rkVcYA1Y",
      "last_name": "Bailey"
    },
    {
      "first_name": "Howard D.",
      "profile_id": "howarddmorgan",
      "sub_title": "Managing Partner & Co-Founder at Argand Partners",
      "location": {
        "short": "New York, New York",
        "city": "New York",
        "country": "United States",
        "default": "New York, New York, United States",
        "state": "New York"
      },
      "industry": "Venture Capital & Private Equity",
      "profile_picture": "https://media.licdn.com/dms/image/C4D03AQHVYRFSO6zTLA/profile-displayphoto-shrink_800_800/0/1600884892971?e=1691625600&v=beta&t=ybGL8Tl5f5VfdyT_HAnbxka0_jGcowedVvaT6f_kcsg",
      "last_name": "Morgan"
    },
    {
      "first_name": "Ian",
      "profile_id": "ian-salmela",
      "sub_title": "Account Executive at Industrial Scientific",
      "location": {
        "short": "Denver Metropolitan Area",
        "city": null,
        "country": "United States",
        "default": "Denver Metropolitan Area",
        "state": null
      },
      "industry": "Business Supplies & Equipment",
      "profile_picture": "https://media.licdn.com/dms/image/D4E03AQHy0IuME5jMbA/profile-displayphoto-shrink_800_800/0/1678924305343?e=1691625600&v=beta&t=Q7l6VzxL-sCqx7--DvL17j-tUMYuTRZCpiBTVUMolHI",
      "last_name": "Salmela"
    },
    {
      "first_name": "Samantha",
      "profile_id": "surioste",
      "sub_title": "Sr. Business Consultant & Executive Coach",
      "location": {
        "short": "New York, New York",
        "city": "New York",
        "country": "United States",
        "default": "New York, New York, United States",
        "state": "New York"
      },
      "industry": "Computer Software",
      "profile_picture": "https://media.licdn.com/dms/image/D4E03AQEvY7jyXvpThA/profile-displayphoto-shrink_800_800/0/1677614571988?e=1691625600&v=beta&t=KlphQ-0f8laau2Bd3R3oYLt-mngcb7n-msSV2ER3A6I",
      "last_name": "Urioste"
    },
    {
      "first_name": "Jeff",
      "profile_id": "jeffdconway",
      "sub_title": "Board Director / Chairman & Company Advisor",
      "location": {
        "short": "Greater Boston",
        "city": null,
        "country": "United States",
        "default": "Greater Boston",
        "state": null
      },
      "industry": "Computer Software",
      "profile_picture": "https://media.licdn.com/dms/image/C4E03AQHH8tTjYNwlig/profile-displayphoto-shrink_800_800/0/1584552981425?e=1691625600&v=beta&t=BN_mxsZJI4IvhqR3NHQxKV1G9QlhJhJGH2r7gYCK1Jo",
      "last_name": "Conway"
    },
    {
      "first_name": "Nathan",
      "profile_id": "nathan-low-8295934a",
      "sub_title": "Angel Investor & Investment Banker",
      "location": {
        "short": "New York, New York",
        "city": "New York",
        "country": "United States",
        "default": "New York, New York, United States",
        "state": "New York"
      },
      "industry": "Financial Services",
      "profile_picture": null,
      "last_name": "Low"
    }
  ]
}

```

</details>

```py
def ScraperAPI(request):
    # When the API endpoint was live, the "with open()..." code block would be replaced by
    # a single line "response = getAPIdata(request, 'position', 'location')"
    with open('./LinkedInScraper/apiresults.json') as r:
        response = json.load(r)
        save_api_data(response)
        db_results = User.Users.all()
        context = {'results': db_results}

        return render(request, "LinkedInScraper/ScraperAPI.html", context)

```

You'll notice that the "save_api_data()" is being called here as well. This method saves all of the API "user results" into the database, which is then passed into the template.

```py
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
```



