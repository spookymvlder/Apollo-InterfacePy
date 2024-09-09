import random



def coin():
    return random.randint(0,1)

def heshe(sex, start):
    if sex == "M":
        pronoun = "he"
    else:
        pronoun = "she"
    if start == 1:
        pronoun = pronoun.title()
    return pronoun

def hisher(sex, start):
    if sex == "M":
        pronoun = "his"
    else:
        pronoun = "her"
    if start == 1:
        pronoun = pronoun.title()
    return pronoun

