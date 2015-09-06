from Conjugate import verb
from random import randrange as r

def limit(number, max = 1689):
    t1 = number + max
    t2 = abs(number - max)
    t3 = t2 - t1
    t4 = t3 / 2
    t5 = abs(t4) - t4
    t6 = t5 / 2
    return t6

def readfile(path = "sorted verbs.txt"):
    with open(path, "rb") as f:
        f = f.read().decode("utf-8").split("\n")
        data = []
        for i in range(len(f)):
            f[i] = f[i].split(" ")
            if len(f[i]) == 2: data.append(f[i])
        for i in range(len(data)):
            data[i][1] = int(data[i][1].split("\r")[0])
    return data

def bigtable():
    table = []
    for i in range(816, 2506):
        table.append([i])
    return table

def addtotable():
    table = bigtable()
    for i in range(len(table)):
        for j in readfile():
            if table[i][0] == j[1]: table[i] = j
    return table

def endtable():
    table = addtotable()
    current = 0
    for i in range(len(table)):
        if len(table[current]) > len(table[i]):
            table[i] = [0, table[i][0]]
            table[i][0] = table[current][0]

        else: current = i
    return table

TABLE_OF_VERBS = endtable()

def gen_possible_moods(chance, outof):
    choose = r(0, outof)
    if choose > chance: f = "Indicative"
    else: f = "Conditional"
    return f

def gen_possible_tenses(mood):
    if mood == "Indicative": possible_tenses = ["Present", "Perfect", "Past", "Future I"]
    else: possible_tenses = ["Present", "Perfect"]
    return possible_tenses

def possible_persons():
    return ["ich", "du", "er", "wir", "ihr", "Sie"]

def choose_verb(score, previous_verb):
    selection = [previous_verb, 0]
    for _ in range(10):
        if selection[0] == previous_verb:
            selection = TABLE_OF_VERBS[r(limit(score-1016), limit(score-616)+1)] # 616 218
    return(selection)

def alternitive_answers(current_verb, mood, tense, person, score):
    tmptbl = list()
    for i in range(6):
        tmptbl.append(i)
    number_of_other_verb_answers = r(2,5)
    other_verb = choose_verb(score, current_verb)[0]
    old_verb = []
    for i in range(number_of_other_verb_answers):
        old_verb.append(tmptbl.pop(r(len(tmptbl))))

    ans1 = verb.Conjugate(current_verb, "Indicative", "Present", possible_persons()[r(6)])
    ans2 = verb.Conjugate(current_verb, "Indicative", "Perfect", possible_persons()[r(6)])
    ans3 = verb.Conjugate(current_verb, "Indicative", "Past", possible_persons()[r(6)])
    ans4 = verb.Conjugate(current_verb, "Indicative", "Future I", possible_persons()[r(6)])
    ans5 = verb.Conjugate(current_verb, "Conditional", "Present", possible_persons()[r(6)])
    ans6 = verb.Conjugate(current_verb, "Conditional", "Perfect", possible_persons()[r(6)])
    answers = [ans1, ans2, ans3, ans4, ans5, ans6]

    real_answer = verb.Conjugate(current_verb, mood, tense, person)

    another_table = []
    for i in range(6): another_table.append(i)

    for i in range(len(answers)):
        if answers[i] == real_answer:
            another_table.pop(i)
            answers[i] = answers[another_table[r(len(another_table))]]

    oans1 = verb.Conjugate(other_verb, "Indicative", "Present", possible_persons()[r(6)])
    oans2 = verb.Conjugate(other_verb, "Indicative", "Perfect", possible_persons()[r(6)])
    oans3 = verb.Conjugate(other_verb, "Indicative", "Past", possible_persons()[r(6)])
    oans4 = verb.Conjugate(other_verb, "Indicative", "Future I", possible_persons()[r(6)])
    oans5 = verb.Conjugate(other_verb, "Conditional", "Present", possible_persons()[r(6)])
    oans6 = verb.Conjugate(other_verb, "Conditional", "Perfect", possible_persons()[r(6)])
    oanswers = [oans1, oans2, oans3, oans4, oans5, oans6]

    aanswers = oanswers
    for i in tmptbl:
        aanswers[i] = answers[i]

    rans = []
    for i in range(len(aanswers)):
        rans.append(aanswers.pop(r(len(aanswers))))
    rans = rans[:3]

    return rans










def gen_question(score, previous_infinitive = " "):
    mood = gen_possible_moods(6, 24)
    tenses = gen_possible_tenses(mood)
    tense = tenses[int(r(4)/3)]
    people = possible_persons()
    person = people[r(len(people))]
    if tense == "Present": multiplier = 0.8
    elif tense == "Perfect": multiplier = 1
    elif tense == "Past": multiplier = 1.5
    elif tense == "Future I": multiplier = 1
    if mood == "Conditional": multiplier *= 1.3
    if person == "ich": multiplier *= 0.9
    elif person == "du": multiplier *= 1
    elif person == "er": multiplier *= 1
    elif person == "wir": multiplier *= 0.9
    elif person == "ihr": multiplier *= 1.2
    elif person == "Sie": multiplier *= 1.1
    if multiplier == 1.3: multiplier = 2
    score = int(0.5+(score / multiplier))
    current_verb = choose_verb(score, previous_infinitive)
    conjugated_verb = verb.Conjugate(current_verb[0], mood, tense, person)
    other_answers = alternitive_answers(current_verb[0], mood, tense, person, score)
    if person == "er":
        person = ["er", "sie", "man"][r(3)]
    if tense == "Past": tense = "Imperfect"
    if tense == "Future I": tense = "Future"
    answer_tense = tense
    question_parts = ["Fill the gap: ", person, " _________ (", current_verb[0], ") in the ", tense.lower(), " tense."]
    if mood == "Conditional":
        question_parts.insert(6, " conditional")
        answer_tense += " conditional"
    question = "".join(question_parts)
    answer = conjugated_verb
    infinitve = current_verb[0]
    question_value = int(0.5+(current_verb[1] * multiplier))
    question = {"answer": answer, "alt answers" : other_answers,
                "question": question, "infinitive" : infinitve, "tense" : answer_tense, "q value" : question_value}

    return question

"""
def Conjugate(verb,mood,tense,person):
        verb: see verbs.txt for possible verbs
        mood: Indicative or Conditional (probs indic)
        tense:
        indicative = ["Present", "Perfect","Past","Pluperfect", "Future I","Future II"]
        conditional = ["Present", "Perfect"]
        person: ich, du, er, wir, ihr, sie, Sie

        er is er, sie and man

        eg verb.Conjugate("tragen", "Indicative", "Present", "ich")

{"ans" : "the answer", "other answers" : ["other ans", "other ans", "other ans", "etc"],
"infinitve" : "infintive", "tense" : "tense"}

"""