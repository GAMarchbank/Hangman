import random


# this function prints the play field. 
def print_play_field(play_field):
    print(f"\n\nA {play_field['A1']}|{play_field['A2']}|{play_field['A3']}\n  -------\nB {play_field['B1']}|{play_field['B2']}|{play_field['B3']}\n  -------\nC {play_field['C1']}|{play_field['C2']}|{play_field['C3']}\n  1|2|3\n\n")

# this function allows the player to make their move
def player_choice(play_field):
    # will contain a list of availble choices
    opt_lst = []
    # contains list of all game tiles
    choice_list = ['a1', 'b1', 'c1', 'a2', 'b2', 'c2', 'a3', 'b3', 'c3']
    # this iterates though the playfield and extracts the ones without a move, appending them to opt_lst
    for keys in play_field:
        if play_field[keys] == ' ':
            opt_lst.append(keys.lower())
    # this section allows user input and makes sure that its a ligitimate move
    while True:
        choice = input('Make your move.\t')
        if choice.lower() not in choice_list:
            print('Unrecognised entry.\nTry again.')
            continue
        elif choice.lower() not in opt_lst:
            print('That position is already taken.\tTry again.')
            continue
        # this section recapilatises the player move before returning it
        else:
            out_string = ''
            for letters in choice.lower():
                if letters == 'a':
                    letters = 'A'
                elif letters == 'b':
                    letters = 'B'
                elif letters == 'c':
                    letters = 'C'
                out_string = out_string + letters
        return out_string

# this function allows the computer to make a move, nothing complicated just a random choice
def computer_choice(play_field):
    opt_lst = []
    for keys in play_field:
        if play_field[keys] == ' ':
            opt_lst.append(keys)
    return random.choice(opt_lst)

# this function checks to see if anyone has won
def victory_check(play_field):
    # a list of all availble winning combinations
    check_lst = [['A1', 'A2', 'A3'],['B1', 'B2', 'B3'], ['C1', 'C2', 'C3'], ['A1', 'B1', 'C1'], ['C2', 'B2', 'A2'], ['A3', 'B3', 'C3'], ['A1', 'B2', 'C3'], ['A3', 'B2', 'C1']]
    # this section moves through the winning combinations and checks to see if any of them contain all one characters
    # for every character the relivent varible is increased by one, if either reach three then that variable triggers the function to return with the winning character
    for lists in check_lst:
        x_num = 0
        o_num = 0
        for items in lists:
            if play_field[items] == 'X':
                x_num += 1
            elif play_field[items] == 'O':
                o_num += 1
        if x_num == 3:
            return 'X'
        elif o_num == 3:
            return 'O'
    return False    

# this funcion checks if there has been a tie
def tie_check(play_field):
    num = 0
    # this section moves through the play field, if it detects a free tile it adds 1 to the num variable
    for keys in play_field:
        if play_field[keys] == ' ':
            num += 1
    # if there are no tiles detected num will be zero, and a tie is returned
    if num == 0:
        return 'tie'

# here the game code begins proper, it is al contained in one while loop
while True:
    # here new game is printed and an empty play field is created
    print('New Game')
    play_field = {'A1': ' ', 'A2': ' ', 'A3': ' ', 'B1': ' ', 'B2': ' ', 'B3': ' ', 'C1': ' ', 'C2': ' ', 'C3': ' '}
    # a random 1/2 choice is created to select if the computer or player will go first
    coin_flip = random.choice([1, 2])
    if coin_flip == 1:
        print('Player goes first.')
    else:
        print('Computer goes first.')
    # here is the main gameplay loop
    while True:
        # at the start of every turn the play field is printed, the game checks for a winner and the game checks if there is a tie by calling on the relivent functions
        print_play_field(play_field)
        win = victory_check(play_field)
        if win  in ['X', 'O']:
            break
        win = tie_check(play_field)
        if win == 'tie':
            break
        # depending on the result of a coin flip the correct order plays out. 
        # the computer_choice and player_choice function are both called to name a key inside the play_field dictionary which is then written with the appropriate letter
        # the game also checks for a tie and a victory again
        if coin_flip == 1:
            play_field[player_choice(play_field)] = 'X'
            print_play_field(play_field)
            win = victory_check(play_field)
            if win in ['X', 'O']:
                break
            win = tie_check(play_field)
            if win == 'tie':
                break
            play_field[computer_choice(play_field)] = 'O'
        else:
            play_field[computer_choice(play_field)] = 'O'
            print_play_field(play_field)
            win = victory_check(play_field)
            if win in ['X', 'O']:
                break
            win = tie_check(play_field)
            if win == 'tie':
                break
            play_field[player_choice(play_field)] = 'X'
    # if the variable win is equal to a relivanet string then the code knows that somebody has one, or that the game is tie and exicutes the apropriate piece of code
    if win == 'X':
        print('Player Victory!!')
    elif win == 'O':
        print('Computer Victory!!')
    elif win == 'tie':
        print('The game was a tie!!')
    # here the code asks if the player would like to play again. if so the loop is restarted if not then the loop breaks and the program exits.
    while True:
        choice = input('Would you like to play again?\t')
        if choice.lower() not in ['yes', 'y', 'no', 'n']:
            print('Unregonised input')
            continue
        break
    if choice.lower() in ['n', 'no']:
        print('Thank you for playing')
        break
    else:
        continue
        
        

            






