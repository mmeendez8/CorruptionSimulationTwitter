
bagofwords = ["pp","alcalde","nngg", "partido", "popular", "populares", "derecha"]

def checkbio (bio):
    bio = bio.lower()
    for w in bagofwords:
        if w in bio: return True
    return False

print checkbio("pp")
