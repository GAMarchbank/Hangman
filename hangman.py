import json
import requests
import random


# this section of the code loads a json list of english words
url = 'https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json'
url_page = requests.get(url)
dictionary = url_page.json()
dictionary = list(dictionary.keys())
# a random word is then selected from the list, before being compared with an online dictionary to ensure that we have a correct definition
while True:
    word = random.choice(dictionary)
    url2 = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    url2_page = requests.get(url2)
    if url2_page.status_code == 200:
        break
# the definition of the selected word is then extracted from the dictionary
url2_page = url2_page.json()
part_of_speech = url2_page[0]['meanings'][0]['partOfSpeech'] 
definitions = [x['definition'] for x in url2_page[0]['meanings'][0]['definitions']]

# the game starts proper here. 
word_keys = len
previous_guesses = []
guesses = 0
victory = False
attempts = 8
print('Welcome to HANGMAN!!\n')
# this is where the main while loop of the game begins
while attempts > 0:
    play_field = []
    # here the player enters their guess, the game will only accept a guess if it passes cirtain requirements
    while True:
        pas = True
        player_guess = input('Choose a letter?\t')
        player_guess = player_guess.lower().replace(' ', '')
        if player_guess == word:
            break
        player_guess = [x for x in player_guess]
        if len(player_guess) > 1:
            print('You can only guess one letter.')
            continue
        for letters in player_guess:
            if letters not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n','o', 'p', 'q', 'r', 's', 't', 'u','v','w','x', 'y','z']:
                print('You can only guess letters.')
                pas = False
            if letters in previous_guesses:
                pas = False
                print('You have already guessed that letter.')
        if player_guess == []:
            print('Please make a guess.')
            continue
        if pas == False:
            continue
        break
    # the player guess is here printed, before being added to the players previous guesses
    print(player_guess)
    previous_guesses = player_guess + previous_guesses
    # here the code checks if the player has guessed the word correctly
    if player_guess == word:
        victory = True
        break
    # here the code checks if the letters the player has already guessed are in the word, if they are the code adds them to a string, if not the code adds _
    for letters in word:
        if letters in previous_guesses:
            play_field.extend(letters)
        else:
            play_field.extend('_')
    # here the code checks the player has made a correct guess, removing an attempt if not
    for letter_guess in player_guess:
        if letter_guess not in [x for x in word]:
            attempts -= 1
    # here the code checks if the player has guessed all of the letters
    if '_' not in play_field:
        victory = True
        break
    # here the code prepares the string for output, before printing the results
    output = ''.join(play_field)
    print(f"You have {attempts} attempts left.")
    print(previous_guesses)
    print(output)
# the code checks if the player has been victorious or not, printing the apropriate message
if victory == True:
    print('Victory!!!\nYou correctly guessed the word.')
else:
    print('Failure!!!\nYou did not manage to guess the word.') 
# here the code prints the definitions of the word
print(f'\nWord:\t\t\t{word}\nType:\t\t\t{part_of_speech}')
for defi in definitions:
    print(f'Definition {definitions.index(defi)+1}:\t\t{defi}')
# here the code prints the final victory message. 
if victory == True:
    print('You have been saved from the noose.')
else:
    print('You have been hung.')    
        
    