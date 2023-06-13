import json


from django.test import TestCase

# Create your tests here.
# testing grounds for methods
# json = {"info": "", "meta":{}, "results:[]"}
# json["results"] = ["firstname"]
r = open('apiresults.json')
response = json.load(r)
jsonObj = response
'''
def saveJsonObj(jsonObj):

    u = User()
    response = jsonObj["results"]
    for user in response:
        u.first_name = user["first_name"]
        u.last_name = user["last_name"]
        u.linkedin_id = user["profile_id"]
        u.company = user["company"]
        u.location = user["location"]["short"]
        u.position = user["sub_title"]
        u.industry = user["industry"]
        print(u)

    return
    '''
def saveJsonObj(jsonObj):
    newDict = {}
    results = jsonObj["results"]
    for i, result in enumerate(results):
        # Iterate through the data and update the dictionary, skip if the key is already in the dictionary
        if result['profile_id'] not in newDict:
            newDict[result['profile_id']] = result

    print(newDict)
    return newDict

saveJsonObj(jsonObj)

