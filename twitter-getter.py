#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees)
#-----------------------------------------------------------------------

from twitter import *
import json

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

#-----------------------------------------------------------------------
# this is the user whose friends we will list
#-----------------------------------------------------------------------
username = "koalakendi"

#-----------------------------------------------------------------------
# perform a basic search
# twitter API docs: https://dev.twitter.com/docs/api/1/get/friends/ids
#-----------------------------------------------------------------------
query = twitter.friends.ids(screen_name = username)

#-----------------------------------------------------------------------
# tell the user how many friends we've found.
# note that the twitter API will NOT immediately give us any more
# information about friends except their numeric IDs...
#-----------------------------------------------------------------------
print "found %d friends" % (len(query["ids"]))

#-----------------------------------------------------------------------
# now we loop through them to pull out more info, in blocks of 100.
#-----------------------------------------------------------------------
for n in range(0, len(query["ids"]), 100):
    ids = query["ids"][n:n+100]

	#-----------------------------------------------------------------------
	# create a subquery, looking up information about these users
	# twitter API docs: https://dev.twitter.com/docs/api/1/get/users/lookup
	#-----------------------------------------------------------------------
    subquery = twitter.users.lookup(user_id = ids)

    # subquery of users/show. It gives info about bio.
    #subquery = twitter.users.show(user_id = ids)
    users_dict = {}
    with open('query_output.json', 'w') as jsonfile:
    	for user in subquery:

            # Create a user dictionary with relevant information given by the key id
            users_dict[user["id"]] = {'name': user['screen_name'], 'bio': user['description'],
                                        'verified': user['verified']}

        json.dump(users_dict, jsonfile, indent=4)
        """
        For loading json files:
        import json
        with open('jsonfile', 'r') as jsonfile:
            my_dictionary = json.load(jsonfile)

        The dictonary returned will be accessed by id as key and will contain
        information about bio, verification and name.
        """
