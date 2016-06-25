# -*- coding: utf-8 -*-
bagofwords = ["pp","alcalde","nngg", "partido", "popular", "populares", "derecha", "nuevas generaciones","concejal","parlamento"]

def checkbio (bio):
    bio = bio.lower()
    for w in bagofwords:
        if w in bio: return True
    return False

def checklocation(location, location_bow):
    location = location.lower().encode('utf-8')
    for valid_location in location_bow:
        if valid_location in location:
            return True
    return False

def load_locations(filename):
    with open(filename, 'r') as locationsfile:
        location_bow = locationsfile.readlines()

    location_bow = [strip_accents(location.strip().lower()) for location in location_bow]

    return location_bow

def strip_accents(s):
    """Since we are analyzing only Spanish we will tackle this problem
    by replacing vowels with accents"""
    subs_accents = {u'á':u'a', u'é':u'e', u'í':u'i',
                    u'ó':u'o', u'ú':u'u'}
    s = s.decode('utf-8')
    s
    for c in s:
        if c in subs_accents.keys():
            s = s.replace(c, subs_accents[c])
    return s.encode('utf-8')
