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

# Primarily for dealing with HTML returns.
def convertbool(value):
    if value == "True" or value == True or value == 1 or value == "true":
        return True
    return False
    
# +/- 10%
def skewvalue(value):
    r = random.uniform(0, .10)
    flip = coin()
    if flip == 1:
        value = value - (value * r)
    else:
        value = value + (value * r)
    return value

def isbool(value):
    if value == True or value == False:
        return True
    return False

