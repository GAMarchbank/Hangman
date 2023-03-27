# Python Miniprojects
These miniprojects I created to both practice and demonstrate my Python skills. 
I have provided extensive notes to show my thought processes during their creation. 
Please feel free to download, run and explore them.

I will be adding the programs to this section below with a breif explination as I upload them.

hangman.py

A simple hangman game that outputs directly into the terminal. While the code for this game isn't particually complicated I enjoyed solving the problem of selecting words for the game to run with. The game starts by requesting data from an online list of english words stored in json format. It then selects a random word from this list and searches for it in an API dictionary. If the word doesn't exist in the dicitonary it selects another random word from the list and repeats the process. This does have the downside of meaning that first few lines of the code can take some time to execute however it means that I can provide greater information on the word chosen. Thus at the end of the game the code prints out the definitions of the word taken from the dictionary. This allows the player to learn a new word if it wasn't in their vocabluary.

noughts_and_crosses.py

A simple noughts and crosses game that outputs directly into the terminal. The game operates around a series of key functions and two while loops. I particually enjoy how compact this piece of code is. Writing the player and computer moves as seperate functions allowed me to create alternative orders for the game without having to write out the code again in long form. This means that even though the code only ever calls upon these functions once per loop there is limited unnecessary code repitition. 

argus_news_scraper.py

A news program that scrapes articals and headlines from my local newspapers website. I created this to expriement with two interlinked moduals, the Requests modual and BeautifulSoup. Using these two moduals together lets code extract data directly off the web and then search through that code to directly extract information. While this program is not complicated the goal of extracted data this way taught me a couple of things. Firstly that the requests modual is not the best method of webscraping in all circumstances. I have since experimented using the selenium modual which though more complicated and slower to run, does appear to have a wider scope of use. Secondly, in creating this program I had to learn the basics of CSS. This proved difficult to do as I went along, so I have decided to learn CSS to make this process quicker in the future.

wiki_date_scrap.py

This program creates and displays a windows popup with information about an individual who died on the current day of the month. It combines several python moduals including requests, BeautifulSoup, BytesIO, win11toast, random, and datetime. The program opens the wikipedia page for the current day of the month, then scrapes a data for notable people who died on that particual day. It then selects one of these people at random and searches their wikipedia page to extract some information about then. This information is then displayed on a windows popup created by win11toast. This program was a joy to create, I particually enjoied combining several python moduals together. One of the major difficulties I had to overcome was the often inconsistant source code of the wikipedia website. Using several try except gateways I was able to create alternative routes for data extraction and also give the program a way of recognising when the source code was too divergent and it should restart witha new individual.
