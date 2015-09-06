#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alex'

from urllib.request import urlopen
import urllib.parse
from html.parser import HTMLParser
import pickle

#-----------------------------------------
#Compilation Functions

def deumlautify(data):
    data = data.replace(b"&auml;", b"ae")
    data = data.replace(b"&uuml;", b"ue")
    data = data.replace(b"&ouml;", b"oe")
    data = data.replace(b"&szlig;", b"ss")

    return data
def defilter(i):
    i = i.replace("ae", "ä")
    i = i.replace("ue", "ü")
    i = i.replace("oe", "ö")
    i = i.replace("ss", "ß")
    return i

def reumlautify(data):

    new_data = [defilter(i) for i in data]
    return new_data

class HTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.data = []

    def handle_data(self, data):
        data = data.splitlines()

        for i in data:
            i = i.strip()

            if i != '' and i != ";":
                self.data.append(i)



def XGen(data, tenses):
    mood = data[0]
    dict = {}
    for tense in tenses:
        #print(tense)
        '''
        i = 0
        while True:
            i+=1
            if data[i]=="ich":
                break
        '''
        i = data.index(tense)
        i+=1
        running = True
        array1 = []
        array2 = []
        while running:

            person = data[i]
            '''
            if person=="Sie":
                running = False
            '''
            verb = data[i+1]
            if verb=="Sie":
                verb=data[i+2]
                array1.append(person)
                array2.append(verb)
                person = "Sie"
                verb = data[i+2]
                running = False

            array1.append(person)
            array2.append(verb)
            i+=2
        tense_entry = {tense:{person:verb for person,verb in zip(array1,array2)}}

        dict.update(tense_entry)

    #print(dict)
    return mood, dict
def Reorder(data, indtenses, contenses):

    Nominal = data[0:data.index("Indicative")]
    #print(Nominal)
    Indicative = data[data.index("Indicative"):data.index("Conjunctive I and II")]
    #print(Indicative)
    Conditional = data[data.index("Conditional"):data.index("Imperative")]
    #print(Conditional)
    #print(Conditional)
    inf = Nominal[Nominal.index("Infinitive:")+1]
    print(inf)
    #print(indtenses)
    Nom, Nom_dict = XGen(Indicative, indtenses)
    #print(Nom)
    #print(Nom_dict)
    Con, Con_dict = XGen(Conditional, contenses)
    #print(Con_dict)
    #print({inf:{Nom:Nom_dict,Con:Con_dict}})
    return {inf:{Nom:Nom_dict,Con:Con_dict}}




def Verb_Conjugate(verb):
    verb = verb.strip().replace(" ","+").lower()
    #verb = verb.encode("unicode-escape")
    print(repr(verb))
    address = "http://www.verbix.com/webverbix/German/{}.html".format(verb)
    #print(address)
    address = urllib.parse.urlsplit(address)
    address = list(address)
    address[2] = urllib.parse.quote(address[2])
    address = urllib.parse.urlunsplit(address)
    #print(address)
    #address = repr(address)#.encode("unicode-escape")
    with urlopen(address) as website:

        # print(html.read())
        html = deumlautify(website.read()).decode("utf8")
        #print(html)

        # print(type(html))


    parser = HTMLParser()
    try:
        parser.feed(html)
    except:
        pass

    try:
        index = parser.data.index("Nominal Forms")
        index2 = parser.data.index("Verbs conjugated like")
    except:
        raise ValueError("Could not connect to Verbix or an invalid verb was passed in")


    data = reumlautify(parser.data[index:index2])
    #print(data)
    indtenses = ["Present", "Perfect","Past","Pluperfect", "Future I","Future II"]
    contenses = ["Present", "Perfect"]

    verb_entry = Reorder(data, indtenses, contenses)
    return verb_entry

def compile():
    with open("verbs.txt") as verb:
        verb_list = verb.readlines()
        verb_list = [i.strip() for i in verb_list]
        print(verb_list)
    magic_dict = {}
    #-----------------------
    #remove
    #verb_list = verb_list[150:]
    print(verb_list)
    for count, i in enumerate(verb_list):
        magic_dict.update(Verb_Conjugate(i))
        print(count)

    with open("verbs.dict","wb") as file:
        pickle.dump(magic_dict, file)
        print("Compiled")

    #print(Reorder(data, indtenses, contenses))
    #print(Nominal)
    #print(Indicative)
    #print(Conditional)

    #print(Verb_Conjugate("tragen"))


#---------------------------------------------------------------------




#Conjugation class

class Verb_Database:
    def __init__(self, dict_path):
        with open(dict_path, "rb") as dict:
            self.verb_dict = pickle.load(dict)

    def Conjugate(self,verb,mood,tense,person):
        """
        verb: see verbs.txt for possible verbs
        mood: Indicative or Conditional
        tense:
            indicative = ["Present", "Perfect","Past","Pluperfect", "Future I","Future II"]
            conditional = ["Present", "Perfect"]
        person: ich, du, er, wir, ihr, sie, Sie
        """

        return self.verb_dict[defilter(verb)][mood][tense][person]

    def Append_Database(verb):
        verb_con = Verb_Conjugate(verb)
        self.verb_dict.update(verb_con)
        pickle.dump(self.verb_dict, "verbs.dict")

verb = Verb_Database("verbs.dict")
verb.Conjugate("verlassen", "Indicative", "Past", "ich")


