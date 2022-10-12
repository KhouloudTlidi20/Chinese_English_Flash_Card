from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#DBC8AC"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/data_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Chinese-english Flash card.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    # print(current_card["Mandarin_Chinese"])
    canvas.itemconfig(card_title, text="Mandarin_Chinese", fill="black")
    canvas.itemconfig(card_word, text=current_card["Mandarin_Chinese"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="Translation", fill="#EDDBC0")
    canvas.itemconfig(card_word, text=current_card["English"], fill="#EDDBC0")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    with open("data/known_words.txt", mode="a", encoding="utf-8") as data:
        data.write(str(current_card["Mandarin_Chinese"]))
        data.write("     ")
        data.write(str(current_card["English"]))
        data.write("\n")
        to_learn.remove(current_card)
        # print(len(to_learn))
        next_card()
        data = pandas.DataFrame(to_learn)
        data.to_csv("data/data_to_learn.csv", index=False)
        next_card()



window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000,func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 24, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 24, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unkown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unkown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
check_button = Button(image=check_image, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

next_card()

window.mainloop()