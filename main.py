from tkinter import *
import json
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
new_data ={}

#-----------------------------------FLIP MECHANISM-----------------------------------#
def flip_card():
    canvas.itemconfig(canvas_image, image=back_card_img)
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_card["English"], fill="white")

#-----------------------------------RANDOMIZE WORD-----------------------------------#
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    new_data = original_data.to_dict(orient="records")
else:
    new_data = data.to_dict(orient="records")

def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(new_data)
    canvas.itemconfig(canvas_image, image=front_card_img)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)

#-----------------------------------SAVE PROGRESS-----------------------------------#
def is_known():
    new_data.remove(current_card)
    data = pandas.DataFrame(new_data)
    data.to_csv("./data/words_to_learn.csv", index=False)
    new_word()

#-----------------------------------UI SETUP-----------------------------------#
window = Tk()
window.title("Flashcard Game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800, bg = BACKGROUND_COLOR, highlightthickness=0)
front_card_img = PhotoImage(file="./images/card_front.png")
back_card_img = PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_card_img)
title_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

my_cross = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=my_cross, highlightthickness=0, command=new_word)
unknown_button.grid(column=0, row=1)
my_tick = PhotoImage(file="./images/right.png")
known_button = Button(image=my_tick, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)

new_word() #so that the first word after running the code is shown on the screen already

window.mainloop()