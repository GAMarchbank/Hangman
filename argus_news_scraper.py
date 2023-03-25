from bs4 import BeautifulSoup
import requests


# the program scrapes the website of my local newspaper, it first extracts lists of articals published on the website. the user selects an article and the program scrapes the text from that article and displays it in the terminal.
# the code beings by calling the beautiful soup moduel on the requested-url and parsing through that data to extract the headlines
url = 'https://www.theargus.co.uk'
articles = BeautifulSoup(requests.get(url).text, 'html.parser').find_all("div", {"class": "mar-small-card__content"})
reading = True
# the main while loop of the artical
while reading:
    dic = {}
    # in this while loop the program creates a variable num which will be both the of the results dictionary and the label that users will use to open an article
    num = 1
    # in this for loop the program searches through the content blocks on the page and extracts the headlines, author names and urls of those articals.
    for items in articles:
        url2 = items.find('a', {'class': 'text-slate no-underline'}).attrs['href']
        soupy = BeautifulSoup(requests.get(url + url2).text, 'html.parser')
        headline = soupy.find('h1', {'class': 'mar-article__headline'}).text
        author = soupy.find('div', {'class': 'author-details__name-container'})
        author_deep = soupy.find('a', {'class': 'author-name mar-mr-1 no-underline'})
        # this scraped data is then printed and put into the dic dictionary with teh key value of the variable num
        if author_deep == None:
            print(f"{num}:\t\t{headline}\n{author.text}\n")
        else:
            print(f"{num}:\t\t{headline}\n{author_deep.text}\n")
        dic[num] = [url + url2]
        num += 1
    print(f"{num}\tExit.")
    # this while loop is where the user interacts with the scraped material
    while True:
        # the user inputs into the variable choice, if this cant be turned into a intiger then the try loop fails and restarts the while loop
        choice = input('What would you like to read?')
        try:
            # if the input = the same as num, then the exit option is detected and the program quits
            choice = int(choice)
            if choice == num:
                print('Exiting Argus News-Brief.')
                reading = False
                break
            # otherwise the program opens the dic dictionary and extracts the relivent url for the artical selected.
            else:
                # the program does another request get and then calls beautiful soup onto that request
                help = dic[choice][0]
                soap = BeautifulSoup(requests.get(help).text, "html.parser")
                # this beautiful soup is then searched for the headline and the text of the article which is then printed for the audience to read
                tex = soap.find('div', {'class': 'article-body'})
                title = soap.find('h1', {'class': 'mar-article__headline'}).text
                print(f"{title}\n{tex.text}")
                # the user then can continue which begins the program all over again.
                input('Continue.')
                break
        except Exception:
            print('Unregcognised command. Please try again.')
            continue
    


