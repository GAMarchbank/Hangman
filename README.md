# Python Miniprojects
These miniprojects I created to both practice and demonstrate my Python skills. 
I have provided extensive notes to show my thought processes during their creation. 
Please feel free to download, run and explore them.

I will be adding the programs to this section below with a breif explination as I upload them.

hangman.py
A simply hangman game that outputs directly into the terminal. While the code for this game isn't particually complicated I enjoyed solving the problem of selecting words for the game to run with. The game starts by requesting data from an online list of english words stored in json format. It then selects a random word from this list and searches for it in an API dictionary. If the word doesn't exist in the dicitonary it selects another random word from the list and repeats the process. This does have the downside of meaning that first few lines of the code can take some time to execute however it means that I can provide greater information on the word chosen. Thus at the end of the game the code prints out the definitions of the word taken from the dictionary. This allows the player to learn a new word if it wasn't in their vocabluary.
