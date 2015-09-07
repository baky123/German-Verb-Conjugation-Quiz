"""
A GUI holder that implements Alex's question generator API
@author Louis Van Steene
"""

from functools import partial
import tkinter as tk
import random
import sys

import Alex_code as questions


class New_Button(tk.Button):
    def __init__(self, parent, **kwargs):
        try:
            self.padx = kwargs["padx"]
        except KeyError:
            self.padx = 0
        try:
            self.pady = kwargs["pady"]
        except KeyError:
            self.pady = 0
        super().__init__(parent, kwargs)
        self.bind("<Enter>", self.Grow)
        self.bind("<Leave>", self.Shrink)

    def Grow(self, arg):
        # print(arg)
        # print("Grow")
        self.xgrow = 3
        self.ygrow = 3
        try:
            self.packx = self.pack_info()["padx"]
            self.packy = self.pack_info()["pady"]
            self.config(padx=self.padx + self.xgrow, pady=self.pady + self.ygrow)
            if self.packx != 0:
                self.pack_configure(padx=self.packx - self.xgrow)
            if self.packy != 0:
                self.pack_configure(pady=self.packy - self.ygrow)
        except:
            self.packx = self.grid_info()["padx"]
            self.packy = self.grid_info()["pady"]
            self.config(padx=self.padx + self.xgrow, pady=self.pady + self.ygrow)
            if self.packx != 0:
                self.grid_configure(padx=self.packx - self.xgrow)
            if self.packy != 0:
                self.grid_configure(pady=self.packy - self.ygrow)

    def Shrink(self, arg):
        # print(arg)
        # print("Grow")

        self.config(padx=self.padx, pady=self.pady)
        try:
            if self.packx != 0:
                self.pack_configure(padx=self.packx)
            if self.packy != 0:
                self.pack_configure(pady=self.packy)
        except:
                if self.packx != 0:
                    self.grid_configure(padx=self.packx)
                if self.packy != 0:
                    self.grid_configure(pady=self.packy)


class Game(tk.Tk):
    def __init__(self):
        # create window
        tk.Tk.__init__(self)
        # set window properties
        self.title("German Verb Conjugations!")
        self.resizable(0, 0)
        # create the initial menu frame
        self.frame = MainMenuFrame(self)
        self.frame.pack()

    def play(self):
        # get rid of menu widgets
        self.frame.pack_forget()
        self.frame.destroy()
        # create gui for the game
        self.frame = PlayFrame(self)
        self.frame.pack()

    def finish(self, p1score, p2score):
        self.frame.pack_forget()
        self.frame.destroy()
        self.frame = GameOverFrame(self, p1score, p2score)
        self.frame.pack()

    def quit(self):
        sys.exit()


class MainMenuFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_gui()

    def create_gui(self):
        tk.Label(self, text="German Verb Game", font=("Cambria", 30)).pack(padx=100, pady=10)
        New_Button(self, text="Spiel", command=self.play, padx=10, pady=10, font=("Calibri", 15)).pack(padx=100, pady=3)
        New_Button(self, text="Ander", command=self.quit, padx=5, pady=7, font=("Calibri", 15)).pack(padx=100, pady=10)

    def play(self):
        self.parent.play()


class PlayFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # set properties (some of these statements can be removed)
        self.parent = parent
        self.qcount = 0
        self.p1LastInfinitive = " "
        self.p2LastInfinitive = " "
        self.p1score = 0
        self.p2score = 0
        self.p1simpleScore = 0
        self.p2simpleScore = 0
        self.p1win = False
        self.p2win = False
        # create the in game GUI layout
        self.create_gui()
        # begin the quiz
        self.next_question()

    def create_gui(self):
        # the questions
        tk.Label(self, name="p1question", text="THIS IS A QUESTION", justify=tk.LEFT, wraplength=150).grid(row=0,
                                                                                                           column=1,
                                                                                                           columnspan=2)
        tk.Label(self, name="p2question", text="THIS IS A QUESTION", justify=tk.RIGHT, wraplength=150).grid(row=0,
                                                                                                            column=4,
                                                                                                            columnspan=2)
        # player 1's score
        tk.Label(self, name="p1score", text="0").grid(row=0, column=0)
        # player 2's score
        tk.Label(self, name="p2score", text="0").grid(row=0, column=6)
        # player 1's answer buttons
        padx = 5
        pady = 5
        New_Button(self, name="abtn1p1", text="ANSWER", command=partial(self.answer, 1, 1)).grid(row=1, column=0,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn2p1", text="ANSWER", command=partial(self.answer, 2, 1)).grid(row=1, column=1,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn3p1", text="ANSWER", command=partial(self.answer, 3, 1)).grid(row=2, column=0,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn4p1", text="ANSWER", command=partial(self.answer, 4, 1)).grid(row=2, column=1,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        # player 2's answer buttons
        New_Button(self, name="abtn1p2", text="ANSWER", command=partial(self.answer, 1, 2)).grid(row=1, column=0 + 5,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn2p2", text="ANSWER", command=partial(self.answer, 2, 2)).grid(row=1, column=1 + 5,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn3p2", text="ANSWER", command=partial(self.answer, 3, 2)).grid(row=2, column=0 + 5,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        New_Button(self, name="abtn4p2", text="ANSWER", command=partial(self.answer, 4, 2)).grid(row=2, column=1 + 5,
                                                                                                 sticky=tk.E + tk.W,
                                                                                                 padx = padx,
                                                                                                 pady = pady)
        # separator
        tk.Frame(self, width=200, bd=1).grid(row=1, rowspan=2, column=2, columnspan=3)
        # status bar
        tk.Label(self, name="status", text=" ").grid(row=3, columnspan=7)
        # next question button
        New_Button(self, name="nextq", text="NEXT QUESTION", bd = 4).grid(row=4, columnspan=7, sticky=tk.E + tk.W, padx = 3, pady = 3)

    def no_next_question(self):
        self.set_status("Wait until both players are ready to go on!")

    def next_question(self):
        self.qcount += 1
        # reset tries
        self.p1tries = 0
        self.p2tries = 0
        # end game after ten questions
        if self.qcount > 10:
            self.end_game()
            return
        self.nametowidget("nextq").config(command=self.no_next_question)
        # generate new questions as dictionaries
        p1dict = questions.generate_question(self.p1score, self.p1LastInfinitive)
        p2dict = questions.generate_question(self.p2score, self.p2LastInfinitive)
        # assign question
        self.p1question = p1dict['question']
        self.p2question = p2dict['question']
        # assign correct answer
        self.p1CorrectAnswer = p1dict['answer']
        self.p2CorrectAnswer = p2dict['answer']
        # assign and randomise all answers
        self.p1Answers = p1dict['alt answers']
        self.p1Answers.append(p1dict['answer'])
        random.shuffle(self.p1Answers)
        self.p2Answers = p2dict['alt answers']
        self.p2Answers.append(p2dict['answer'])
        random.shuffle(self.p2Answers)
        # assign previous infinitives
        self.p1LastInfinitive = p1dict['infinitive']
        self.p2LastInfinitive = p2dict['infinitive']
        # assign previous difficulties
        self.p1LastDifficulty = p1dict['q value']
        self.p2LastDifficulty = p2dict['q value']
        # finally, update the GUI
        self.update()

    def answer(self, btn, player):
        if player == 1:
            if self.p1win:
                self.set_status("You have already got the answer right!")
                return
            if self.p1Answers[btn - 1] == self.p1CorrectAnswer:
                self.set_status("Player 1 has entered an correct answer in " + str(self.p1tries + 1) + " attempts")
                self.p1win = True
                self.p1simpleScore += 1
                if self.p1tries == 0:
                    points = 1
                elif self.p1tries == 1:
                    points = 0.33
                elif self.p1tries == 2:
                    points = 0.1
                else:
                    points = 0
                self.p1score = questions.adjust(self.p1score, self.p2LastDifficulty, points)
            else:
                self.p1tries += 1
                self.p1win = False
                self.set_status("Player 1 has entered an incorrect answer. Attempts: " + str(self.p1tries))
        if player == 2:
            if self.p2win:
                self.set_status("You have already got the answer right!")
                return
            if self.p2Answers[btn - 1] == self.p2CorrectAnswer:
                self.set_status("Player 1 has entered an correct answer in " + str(self.p2tries + 1) + " attempts")
                self.p2win = True
                self.p2simpleScore += 1
                if self.p2tries == 0:
                    points = 1
                elif self.p2tries == 1:
                    points = 0.33
                elif self.p2tries == 2:
                    points = 0.1
                else:
                    points = 0
                self.p2score = questions.adjust(self.p2score, self.p2LastDifficulty, points)
            else:
                self.p2tries += 1
                self.p2win = False
                self.set_status("Player 2 has entered an incorrect answer. Attempts: " + str(self.p2tries))
        if self.p1win and self.p2win:
            self.p1win = False
            self.p2win = False
            self.set_status("Click for next question when ready!")
            self.nametowidget("nextq").config(command=self.next_question)

    def set_status(self, string):
        self.nametowidget("status").config(text=string)

    def update(self):
        # update the player's scores, the questions, the answers
        # scores
        self.nametowidget("p1score").config(text=str(self.p1score))
        self.nametowidget("p2score").config(text=str(self.p2score))
        # questions
        self.nametowidget("p1question").config(text=self.p1question)
        self.nametowidget("p2question").config(text=self.p2question)
        # buttons
        self.nametowidget("abtn1p1").config(text=self.p1Answers[0])
        self.nametowidget("abtn2p1").config(text=self.p1Answers[1])
        self.nametowidget("abtn3p1").config(text=self.p1Answers[2])
        self.nametowidget("abtn4p1").config(text=self.p1Answers[3])
        self.nametowidget("abtn1p2").config(text=self.p2Answers[0])
        self.nametowidget("abtn2p2").config(text=self.p2Answers[1])
        self.nametowidget("abtn3p2").config(text=self.p2Answers[2])
        self.nametowidget("abtn4p2").config(text=self.p2Answers[3])

    def end_game(self):
        self.parent.finish(self.p1score, self.p2score)


class GameOverFrame(tk.Frame):
    def __init__(self, parent, p1score, p2score):
        tk.Frame.__init__(self, parent)
        self.p1score = p1score
        self.p2score = p2score
        if p1score > p2score:
            self.string = "Player 1 (on the left) has won!"
        else:
            self.string = "Player 2 (on the right) has won!"
        self.create_gui()

    def create_gui(self):
        tk.Label(self, text="PLAYER 1").grid(row=0, column=0)
        tk.Label(self, text="PLAYER 2").grid(row=0, column=1)
        tk.Label(self, text=str(self.p1score)).grid(row=1, column=0)
        tk.Label(self, text=str(self.p2score)).grid(row=1, column=1)
        tk.Label(self, text=self.string).grid(row=2, columnspan=2)
        New_Button(self, text="RESTART", command=restart).grid(row=3, columnspan=2)


def restart():
    global root
    root.destroy()
    root = Game()
    root.mainloop()


if __name__ == "__main__":
    root = Game()
    root.mainloop()
