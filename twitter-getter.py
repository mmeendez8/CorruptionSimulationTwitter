#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-friends
#  - lists all of a given user's friends (ie, followees)
#-----------------------------------------------------------------------

from twitter import *
import json
from utils import *
import os
import logging

try:
    os.remove("query_output.json")
except OSError:
    pass

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
config = {}
execfile("config_barb.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(
        auth = OAuth(config["access_key"], config["access_secret"],
         config["consumer_key"], config["consumer_secret"]), retry = True)

config_list = ['config_barb.py', 'config_lidon.py', 'config_mama.py', 'config_papa.py', 'config_jesu.py', 'config4.py', 'config5.py']
swap_counter = 0

# Configure logging file for debugging Twitter error response
logging.basicConfig(filename='catched_responses.log',level=logging.DEBUG)

# Starting point
username = "ppmadrid"
#network_sizes = [2000, 3000, 4000, 5000]
network_sizes = range(250,10000,250)
# Recursive parameters
visited = []
tovisit = [username]
count = 1;
users_dict = {}

user = twitter.users.show(screen_name=username)
users_dict[user["id"]] = {'name': user['screen_name'], 'bio': user['description'],
                        'verified': user['verified'], 'node': count, 'neighbours':[],
                        'real_name': user['name'], 'location':user['location'],
                        'followers': user['followers_count']}
tovisit = [user["id"]]

# Load the location restrictions in a bag of words vector
location_bow = load_locations('municipios_madrid.txt')
##########################
#PROBLEM: FIRST USER IS NOT IN JSON FILE
##########################
user_count = 0
while (tovisit and count<max(network_sizes)):
    # If all the jsons are built, finish.
    if not network_sizes:
        break

    if twitter.application.rate_limit_status()["resources"]["friends"]["/friends/ids"]["remaining"] < 2:
        swap_counter+=1
        config = {}
        print 'Swapping account'
        print config_list[swap_counter % len(config_list)]
        print
        execfile(config_list[swap_counter % len(config_list)], config)
        twitter = Twitter(
                auth = OAuth(config["access_key"], config["access_secret"],
                 config["consumer_key"], config["consumer_secret"]), retry = True)

    # Searh followers
    try:
        query = twitter.friends.ids(user_id = tovisit[0])
    except TwitterHTTPError as e:
        logging.debug('Error obtaining friends list from id: ' + str(tovisit[0]))
        logging.debug(e)
    # Remove user from tovisit
    visited.append(tovisit.pop(0));
    ####
    # Counter of how many different users analyzed
    user_count+=1
    print 'Users visited: '+str(user_count)
    ####
    # Number of followers
    print "found %d friends" % (len(query["ids"]))

    # Loop through followers in blocks of 100
    for n in range(0, len(query["ids"]), 100):
        ids = query["ids"][n:n+100]
        # If network size reached break the subqueries
        #if count >= network_sizes[0]: break
    	# Information of each of the followers

        if twitter.application.rate_limit_status()["resources"]["users"]["/users/lookup"]["remaining"] < 5:
            swap_counter+=1
            config = {}
            print 'Swapping account'
            execfile(config_list[swap_counter % len(config_list)], config)
            twitter = Twitter(
                    auth = OAuth(config["access_key"], config["access_secret"],
                     config["consumer_key"], config["consumer_secret"]), retry = True)

        try:
            subquery = twitter.users.lookup(user_id = ids)
        except TwitterHTTPError as e:
            logging.debug('Error performing lookup with ids: '+str(ids))
            logging.debug(e)



        for user in subquery:
            # If user biography has certain keywords
            if (checkbio(user['description']) and checklocation(user['location'], location_bow)):
                #HERE WE HAVE TO ADD THE CONNECTION

                # Check if it is a new user
                if ((user['id'] not in visited) and (user['id'] not in tovisit)):
                    count+=1;
                    print count
                    tovisit.append(user['id'])
                    # Create a user dictionary with relevant information given by the key id
                    users_dict[user["id"]] = {'name': user['screen_name'], 'bio': user['description'],
                                            'verified': user['verified'], 'node': count,
                                            'neighbours':[visited[-1]], 'real_name': user['name'],
                                            'location':user['location'],
                                            'followers_count': user['followers_count']}
                    #print user['location'].encode('utf-8')
                    #print user['name'].encode('utf-8')
                elif (user['id'] in visited):
                    #print user['screen_name']
                    users_dict[user['id']]['neighbours'].append(visited[-1])

    # With this approach we avoid computing the same network for bigger networks iteratively
    if count>=network_sizes[0]:
        with open('query_output'+str(network_sizes[0])+'.json', 'a') as jsonfile:
            json.dump(users_dict, jsonfile, indent=4)
        network_sizes.pop(0)
