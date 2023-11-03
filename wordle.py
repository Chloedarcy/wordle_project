from tkinter import messagebox
import tkinter as tk
import random
from words import wordList, alphabetList

#Create windows and frames
window = tk.Tk()
window.title('Wordle')
window.configure(bg='#1f1c1c')
window.geometry("560x900")
frame = tk.Frame(window)
frame.configure(bg='#1f1c1c') 
frame.pack(side='bottom')

#Font and Color variables
darkGrey = '#1f1c1c'
lightGrey = '#4f4f4f'
offWhite = '#ebe8e8'
green = '#407a49'
yellow = '#ccb837'
foregroundColor = 'white'
backgroundColor = darkGrey
#passedColor = lightGrey
mode = 'dark'
count = 0
font = 'Helvetica, 30'
keys = []

#Other Variables
letters = []
letter_count = 0
guess = ''
winner = False
num = 0
word = random.choice(wordList)
print(word)

def layout():
    global gridLabel, wordleLabel, questionButton, darkOrLightButton, keyboardLabel

    #Creates the labels for the grids to go on top of
    gridLabel = tk.Label(frame, bg = backgroundColor)
    keyboardLabel = tk.Label(frame, bg = backgroundColor)
    wordleLabel = tk.Label(window, bg = backgroundColor, height = 10, borderwidth=2, fg = foregroundColor, relief="solid", 
                            highlightthickness=1, highlightbackground=foregroundColor, text = 'Wordle', font = 'Helvetica, 30')
    
    wordleLabel.pack(side='top', fill='x')
    gridLabel.pack()
    keyboardLabel.pack()

    #Create the a button for light or dark mode and a question box
    questionButton = tk.Button(wordleLabel, text = '?', fg = 'white', bg = darkGrey, activeforeground = foregroundColor, 
                                activebackground = backgroundColor, command=question)
    darkOrLightButton = tk.Button(wordleLabel, text = '𖤓', fg = 'white', bg = darkGrey, activeforeground = foregroundColor, 
                                    activebackground = backgroundColor, command=lightOrDarkMode)
    darkOrLightButton.place(x=460, y=10)
    questionButton.place(x=510, y=10)
    grid()
    
def grid():
    global btn, keys, key
    #Create the main grid
    for i in range(30):
        btn = tk.Button(gridLabel, text=' ', fg= foregroundColor, width=1, bg= backgroundColor,
                        activeforeground = foregroundColor, activebackground= backgroundColor, font=font)
        btn.grid(row=i//5, column=i%5, padx=3, pady=5)
        letters.append(btn)
    
    #Create the keyboard
    for i in range(len(alphabetList)):
        #Change the row and columns accordingly
        if i < 10:
            row = 0
            col = i
        elif i < 19:
            row = 1
            col = i - 10
        else:
            row = 2
            col = i - 19
        key = tk.Button(keyboardLabel, text=alphabetList[i], height=2, width=2, fg=foregroundColor, bg=backgroundColor,
                        activeforeground=foregroundColor, activebackground=backgroundColor, font='Helvetica, 10')
        key.bind("<Button-1>", screen_key_pressed)  # Bind the function to the button
        key.grid(row=row, column=col, padx=3, pady=5)  # Place the button in the grid
        keys.append(key)

def screen_key_pressed(event): 
    global letter_count, guess, num, guess, letters
    #Make the buttons of the keyboard functional
    if event.widget["text"] != "⌫" and  event.widget["text"] != "Enter" :
        if not winner:
            if  event.widget["text"] >= 'A' and  event.widget["text"] <= 'Z':
                if letter_count < 5:
                    #Add the letters to the screen
                    letters[letter_count + num]['text'] = event.widget["text"]
                    letters[letter_count + num].focus()
                    guess = guess +  event.widget["text"]
                    letter_count += 1
    #Press enter to submit a word
    if (letter_count % 5) == 0 and event.widget["text"] == "Enter":
        check_word(guess)
        if guess.lower() == word:
            print('end game')
        else:
            guess = ''
            go_again()
    if event.widget["text"] == '⌫':
        letters[letter_count + num -1]['text'] = ''
        letter_count -= 1
        guess = guess[:-1]
    keyboardColors()

def key_pressed(event):
    #Take input through the computer keyboard
    global letter_count, guess, num, guess
    if not winner:
        if event.char >= 'a' and event.char <= 'z' or event.char >= 'A' and event.char <= 'Z':
            if letter_count < 5:
                #Add letters to the screen
                letters[letter_count + num]['text'] = event.char.upper()
                letters[letter_count + num].focus()
                guess = guess + event.char.upper()
                letter_count += 1

        #Press enter to submit a five letter word
        if letter_count % 5 == 0 and event.keycode == 36 and letters[num]['text'] != ' ':
            check_word(guess)
            if guess.lower() == word:
                print('end game')
            else:
                guess = ''
                go_again()
        keyboardColors()

def delete(event):
    #Use the delete key on the pysical keyboard
    global deleted, letter_count, num, guess
    if event and letter_count > 0:
        letters[letter_count + num - 1]['text'] = ''
        letter_count -= 1
        guess = guess[:-2]

def keyboardColors():
    global passedColor
    #Set passedColor
    if mode == 'dark':
        passedColor = lightGrey
    else: 
        passedColor = offWhite
    #Change the colors of the keyboard display if a letter is used
    for i, letter in enumerate(letters):
        for j, key in enumerate(keys):
            #Correspond the letters input and their result to the keyboard color backgrounds
            if letters[i]['bg'] == green:
                if keys[j]["text"] == letters[i]["text"]:
                    keys[j].configure(bg = green, activebackground = green, fg = foregroundColor)
            elif letters[i]['bg'] == yellow:
                if keys[j]["text"] == letters[i]["text"]:
                    keys[j].configure(bg = yellow, activebackground = yellow, fg = foregroundColor)
            elif (letters[i]['bg'] == offWhite) or (letters[i]['bg'] == lightGrey):
                if keys[j]["text"] == letters[i]["text"]:
                    keys[j].configure(bg = passedColor, fg = foregroundColor, activebackground = passedColor)
            if keys[j]['bg'] == foregroundColor:
                keys[j].configure(bg = backgroundColor, fg = foregroundColor, activebackground = backgroundColor, activeforeground = foregroundColor) 

def go_again():
    #Change values to move to next line
    global num, letter_count
    letter_count = 0
    num += 5

def check_word(guess):
    global winner, mode
    count = 0
    if mode == 'dark':
        bg = lightGrey
    else:
        bg = offWhite
    #Assign colors based on if the letters/words are correct
    for i, letter in enumerate(guess):
        if letter.lower() == word[i]:
            letters[i + num]['bg'] = green
            letters[i + num]['activebackground'] = green
        elif letter.lower() in word:
            #If a letter is there twice, only make it yellow once
            if guess.count(letter.upper()) >= 2 and count == 0:
                letters[i + num]['bg'] = yellow
                letters[i + num]['activebackground'] = yellow
                count += 1
            elif guess.count(letter.upper()) == 1:
                letters[i + num]['bg'] = yellow
                letters[i + num]['activebackground'] = yellow
            else:
                letters[i + num]['bg'] = bg
                letters[i + num]['activebackground'] = bg
        else:
            letters[i + num]['bg'] = bg
            letters[i + num]['activebackground'] = bg
    if guess == word:
        winner = True

def question():
    #Show instructions when the question box is pressed
    questionBox = tk.Tk()
    questionBox.title("Instructions")
    questionBox.geometry("380x480+100+100")
    questionsText1 = tk.Label(questionBox, height = 3, width = 90, bg = backgroundColor, fg = foregroundColor,text = 'How To Play:\n', font = 'Helvetica, 20')
    questionsText2 = tk.Label(questionBox, height = 18, width = 100, bg = backgroundColor, fg = foregroundColor, text = '- Guess the wordle in 6 tries\n - Each guess must be a valid 5 letter word\n - The color of the tiles will change\n to show how close your guess was to the word\n - Yellow means the letter is in the word,\n but not in the right space\n - Green means the letter is in the right place \n - Grey means the letter is not in the word' , font = 'Helvetica, 12', anchor='n')  

    questionsText1.pack()
    questionsText2.pack()

def lightOrDarkMode():
    #Switches light and dark mode (colors)
    global backgroundColor, foregroundColor, frame, count, mode, passedColor
    #Set Colors
    if mode == 'dark':
        mode = 'light'
        backgroundColor = 'white'
        foregroundColor = darkGrey
        passedColor = offWhite
        keyboardColors()
    else: 
        mode = 'dark'
        backgroundColor = darkGrey
        foregroundColor = 'white' 
        passedColor = lightGrey
        keyboardColors()
    #Ajust the colors of everything
    for i, letter in enumerate(letters):
        if letters[i]['bg'] == lightGrey or letters[i]['bg'] == offWhite:
            letters[i].configure(bg=passedColor, fg=foregroundColor, activeforeground=foregroundColor, activebackground=passedColor)
        if letters[i]['bg'] == foregroundColor:
            letters[i].configure(bg=backgroundColor, fg=foregroundColor, activeforeground=backgroundColor, activebackground=backgroundColor)
    window.configure(bg=backgroundColor)
    frame.configure(bg=backgroundColor) 
    gridLabel.configure(bg=backgroundColor)
    wordleLabel.configure(bg=backgroundColor, fg=foregroundColor)
    keyboardLabel.configure(bg=backgroundColor)
    questionButton.configure(bg=backgroundColor, fg=foregroundColor, activebackground=backgroundColor, activeforeground = foregroundColor)
    darkOrLightButton.configure(bg=backgroundColor, fg=foregroundColor, activebackground=backgroundColor, activeforeground = foregroundColor)

#Bind the keys and call functions
window.bind('<BackSpace>',delete)
window.bind('<Key>', key_pressed)
layout()
window.mainloop()