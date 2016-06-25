
bagofwords = ["pp","alcalde","nngg", "partido", "popular", "populares", "derecha", "nuevas generaciones","concejal","parlamento"]

def checkbio (bio):
    bio = bio.lower()
    for w in bagofwords:
        if w in bio: return True
    return False

def checklocation(location):
    pass
