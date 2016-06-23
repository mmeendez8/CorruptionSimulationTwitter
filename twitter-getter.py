#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees)
#-----------------------------------------------------------------------

from twitter import *
import json
from utils import checkbio
import os

try:
    os.remove("query_output.json")
except OSError:
    pass

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
        auth = OAuth(config["access_key"], config["access_secret"], config["consumer_key"], config["consumer_secret"]))



# Starting point
username = "ppmadrid"

# Recursive parameters
visited = []
tovisit = [username]
count = 1;
users_dict = {}

user = twitter.users.show(screen_name=username)
users_dict[user["id"]] = {'name': user['screen_name'], 'bio': user['description'],
                        'verified': user['verified'], 'node': count}
tovisit = [user["id"]]
##########################
#PROBLEM: FIRST USER IS NOT IN JSON FILE
##########################

while (tovisit and count<1000):
    # Searh followers
    query = twitter.friends.ids(user_id = tovisit[0])
    # Remove user from tovisit
    visited.append(tovisit.pop(0));

    # Number of followers
    print "found %d friends" % (len(query["ids"]))

    # Loop through followers in blocks of 100
    for n in range(0, len(query["ids"]), 100):
        ids = query["ids"][n:n+100]

    	# Information of each of the followers
        subquery = twitter.users.lookup(user_id = ids)

        with open('query_output.json', 'a') as jsonfile:
            for user in subquery:
                # If user biography has certain keywords
                if checkbio(user['description']):
                    #HERE WE HAVE TO ADD THE CONNECTION

                    # Check if it is a new user
                    if ((user['id'] not in visited) and (user['id'] not in tovisit)):
                        count+=1;
                        tovisit.append(user['id'])
                        # Create a user dictionary with relevant information given by the key id
                        users_dict[user["id"]] = {'name': user['screen_name'], 'bio': user['description'],
                                                'verified': user['verified'], 'node': count
                                                'neighbours':[visited[-1]]}

json.dump(users_dict, jsonfile, indent=4)


        """
        For loading json files:
        import json
        with open('jsonfile', 'r') as jsonfile:
            my_dictionary = json.load(jsonfile)

        The dictonary returned will be accessed by id as key and will contain
        information about bio, verification and name.
        """
