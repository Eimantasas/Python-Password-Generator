from tkinter import *
import random
from PIL import Image, ImageTk


def insertstring(index, string, str_to_insert):
    return string[:index] + str_to_insert + string[index:]

def generate():
    randquestlist = open('questions.txt', 'r')
    randchance = random.randint(1, 100)
    if randchance == 7:
        innsjekkslabel.config(text="", image=image_tk)
    else:
        randquestlist = list(randquestlist)
        rand_question = random.choice(randquestlist)
        length = len(rand_question)
        maxlength = 30
        indexofquestion = maxlength
        if length >= maxlength:
            while True:
                if list(rand_question)[indexofquestion] == " ":
                    rand_question = insertstring(indexofquestion, rand_question, "\n")
                    break
                else:
                    indexofquestion -= 1
                    continue
        innsjekkslabel.config(text=rand_question, image="")


window = Tk()
window.title("Innsjekks Generator")
window.geometry('1070x320')

image_original = Image.open('goofycat.png').resize((100, 100))
image_tk = ImageTk.PhotoImage(image_original)

innsjekkslabel = Label(window, text="Innsjekkspørsmål skal generere her", font=("arial", 40))
genererbutton = Button(window, text="Generer", font=("arial", 25), command=generate)
imglabel = Label(image=image_tk)

innsjekkslabel.pack(pady=(50, 20))
genererbutton.pack(pady=25)

window.mainloop()