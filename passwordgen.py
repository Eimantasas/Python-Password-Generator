from tkinter import *
from tkinter import messagebox
import random



def randomcase(word: str) -> str:
    '''
    Randomizes capitalization in a word
    '''
    result = ''
    for c in word:
        case = random.randint(0, 1)
        if case == 0:
            result += c.upper()
        else:
           result += c.lower()
    return result

def showhidepass():
    '''
    Function for the button that hides/shows your generated password
    '''
    global passhidden
    if newpasword != "":
        if passhidden:
            label2.config(text=newpasword)
            showhidepassbutton.config(text="Hide Password")
            passhidden = False
        else:
            label2.config(text="Password Hidden")
            showhidepassbutton.config(text="Show Password")
            passhidden = True

def check_userpass(userpass: str) -> bool:
    '''
    Checks if the password fits all the selected preferences
    '''

    chosenupper = upperbool.get()
    chosenlower = lowerbool.get()
    chosennumbers = numberbool.get()
    chosensymbols = symbolbool.get()

    if chosenlower:
        has_lower = userpass.upper() != userpass
    else:
        has_lower = True
    if chosenupper:
        has_upper = userpass.lower() != userpass
    else:
        has_upper = True
    if chosennumbers:
        has_number = any(ch.isdigit() for ch in userpass)
    else:
        has_number = True
    if chosensymbols:
        has_symbol = any(ch in "!$%^&*()-_=+#" for ch in userpass)
    else:
        has_symbol = True

    return has_lower and has_upper and has_number and has_symbol

def clear():
    '''
    Clears the password
    '''
    global newpasword
    global password
    password = ""
    newpasword = ""
    label2.config(text=password)

def copy():
    '''
    Copies the password to clipboard
    '''
    global newpasword
    window.clipboard_clear()
    window.clipboard_append(newpasword)

def submit():
    '''
    Handles all the info that was put in and generates a password using it
    '''
    global newpasword
    global password
    length = 0
    randomcharlist = ""
    attempts = 0

    chosenupper = upperbool.get()
    chosenlower = lowerbool.get()
    chosennumbers = numberbool.get()
    chosensymbols = symbolbool.get()
    chosenrandcap = randcapbool.get()

    passkeyword = entry2.get()

    #Preferanser
    if chosenupper == True:
        randomcharlist += randomcharsupper

    if chosenlower == True:
        randomcharlist += randomcharslower

    if chosennumbers == True:
        randomcharlist += randomnumbers

    if chosensymbols == True:
        randomcharlist += randomsymbols


    if chosenrandcap:
        passkeyword = randomcase(passkeyword)

    length = int(clickedoptions.get())
    if length >= minimumpasslen and length <= maximumpasslen and randomcharlist != "" and len(passkeyword) <= length:
        length = length - len(passkeyword)
        while True:
            password = ""
            for i in range(0, length):
                password = password + random.choice(randomcharlist)
            newpasword = passkeyword + password
            eligiblepassword = check_userpass(newpasword) #THe program crashes if it doesn't have enough space for the chosen preferenses
            if attempts >= 1000: #Not the best fix, but its something atleast
                eligiblepassword = True
                messagebox.showwarning("Alert!", " Alert! Not enough space for your selected preferences. Password might have generated incorrectly.")
            if eligiblepassword:
                break
            else:
                attempts += 1
                continue
        print(attempts)
        if passhidden:
            label2.config(text="Password generated (hidden)")
        else:
            label2.config(text=newpasword)
        password = ""
        errorlabel.pack_forget()
    else:
        errorlabel.config(text="Invalid amount of characters (" + str(minimumpasslen) +"-"+ str(maximumpasslen) +" characters) OR none of the options selected \n (Uppercase, lowercase, numbers, symbols). You must select atleast 1")
        errorlabel.pack()
    password = ""

window = Tk()
window.title("RPG (Random Password Generator, not the rocket launcher)")
window.geometry('720x620')

randomcharsupper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
randomcharslower = "abcdefghijklmnopqrstuvwxyz"
randomnumbers = "0123456789"
randomsymbols = "!@#$%^&*()"
password = ""
newpasword = ""
passhidden = True

minimumpasslen = 8
maximumpasslen = 20
lengthoptions = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
clickedoptions = StringVar()
clickedoptions.set(lengthoptions[0])

upperbool = BooleanVar()
lowerbool = BooleanVar()
numberbool = BooleanVar()
symbolbool = BooleanVar()
randcapbool = BooleanVar()


dropchoicebutton = OptionMenu(window, clickedoptions, *lengthoptions)
dropchoicebutton.config(width=10)

label1 = Label(window,
               text="how many characters should your password be? (" + str(minimumpasslen) +"-"+ str(maximumpasslen) +" characters)",
               font=("arial", 20))

entry2 = Entry(window,
               font=('arial', 20))

label2 = Label(window,
               text="[Random Password will generate here]",
               font=('arial', 20))

keywordlabel = Label(window,
                     text="Type in a keyword that you will rememember here",
                     font=('arial', 20))

errorlabel = Label(window,
               text="Password length requirements not met (" + str(minimumpasslen) +"-"+ str(maximumpasslen) +" characters)",
               fg="red")

submitbutton = Button(window,
                      text="submit",
                      command=submit)

copybutton = Button(window,
                    text="Copy Password",
                    command=copy)

clearpassbutton = Button(window,
                         text="Clear Password",
                         command=clear)

showhidepassbutton = Button(window,
                         text="Show Password",
                         command=showhidepass)

checkbuttonupper = Checkbutton(window,
                               text="Uppercase",
                               variable=upperbool,
                               onvalue=True,
                               offvalue=False)

checkbuttonlower = Checkbutton(window,
                               text="Lowercase",
                               variable=lowerbool,
                               onvalue=True,
                               offvalue=False)

checkbuttonnumbers = Checkbutton(window,
                               text="Numbers",
                               variable=numberbool,
                               onvalue=True,
                               offvalue=False)

checkbuttonsymbols = Checkbutton(window,
                               text="Symbols",
                               variable=symbolbool,
                               onvalue=True,
                               offvalue=False)

checkbuttonrandcap = Checkbutton(window,
                               text="Randomize Capitalization (for keyword)",
                               variable=randcapbool,
                               onvalue=True,
                               offvalue=False)


keywordlabel.pack(pady=(20, 3))
entry2.pack(pady=5)
checkbuttonrandcap.pack(pady=5)
label1.pack(pady=(30, 3))
dropchoicebutton.pack(pady=(5, 20))
checkbuttonlower.pack(pady=5)
checkbuttonupper.pack(pady=5)
checkbuttonnumbers.pack(pady=5)
checkbuttonsymbols.pack(pady=5)
submitbutton.pack(pady=5)
label2.pack(pady=10)
copybutton.pack(pady=5)
clearpassbutton.pack(pady=5)
showhidepassbutton.pack(pady=5)

window.mainloop()
