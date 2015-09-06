from Question_Generator import gen_question
from Real_Life_Elo import predictedoutcome
from Real_Life_Elo import adjust as aj


def generate_question(player_score, previous_infinitive = " "):
    """
    this function takes the player's current score, and the pervious infinive
    (if available) and returns a question along with it difficulty in the form of a dictionary.
    the dictionary has the following entries:
{
        "answer" : the correct answer (string),
        "alt answers" : [a, list, of, 3, other, answers, (which are strings)],
        "question": the question (string),
        "infinitive" : the infinitive for this question (string) (possiblly redundent),
        "tense" : the tense for this question (string) (possiblly redundent),
        "q value" : the elo rating of the question (int)}

    """
    dictionary = gen_question(player_score, previous_infinitive)
    return dictionary

def adjust(player_score, question_dificulty, how_well_the_player_did):
    """
    this function takes the player's score, the dificulty of the question being
    asked, and a rating of how well the player did on the previous question on a
    scale of 0 to 1 (with 1 being they won and 0 being they lost).

    (If the player gets the answer right the first time they get 1 point,
    If the player gets the answer right the second time they get 0.33 points,
    If the player gets the answer right the third time they get 0.1 points,
    If the player gets the answer right the last time they get 0 points)

    this function then returns the player's updated score and as such their score
    should be set to this value
    - ie current_player_score = adjust(current_player_score, dict["q value"], success_level)
    or something to that end. (this example assumes that the dictionary that the
    question was stored in is called dict and that how well the player did at
    answering that question is represented by the success_level variable)


    """

    #the chance that the player wins:
    player_winning_chance = predictedoutcome(player_score, question_dificulty)

    #works out what the player's new score should be
    new_player_score = aj(player_score, player_winning_chance, how_well_the_player_did)
    return new_player_score
