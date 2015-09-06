import random, math



def predictedoutcome(elo1, elo2):
    return 1/(1+(math.pow(10, ((elo2-elo1)/400))))

def adjust(current, expected, actual):
    k = 0                                                                       # maybe 800/(games played in the last x amount of time)
    if current < 200: k = 40
    elif current >= 200 and current < 400: k = 38
    elif current >= 400 and current < 600: k = 36
    elif current >= 600 and current < 800: k = 34
    elif current >= 800 and current < 1000: k = 32
    elif current >= 1000 and current < 1200: k = 30
    elif current >= 1200 and current < 1400: k = 28
    elif current >= 1400 and current < 1600: k = 26
    elif current >= 1600 and current < 1800: k = 24
    elif current >= 1800 and current < 2000: k = 22
    elif current >= 2000 and current < 2200: k = 20
    elif current >= 2200 and current < 2400: k = 18
    elif current >= 2400 and current < 2600: k = 16
    elif current >= 2600 and current < 2800: k = 14
    elif current >= 2800 and current < 3000: k = 12
    current = current + k*(actual - expected)
    return int(current)
