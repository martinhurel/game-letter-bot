from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
import os
import unidecode

import csv

dico = []
with open("liste_francais.csv") as f:
    txt = csv.reader(f, delimiter='\n')
    for line in txt:
        word = line[0]
        word = unidecode.unidecode(word) # Remove accents
        if word[0].islower(): # If word not proper noun
            if word.count(' ') == 0: # If no space in word
                dico.append(word.upper())

dico.sort(key=len, reverse= True)

PATH = '/Users/hurelmartin/Git-Repo/game-letter-bot/chromedriver'

#Change the code for every new session
game_code = "CDVT"

driver = webdriver.Chrome(PATH)

driver.get(f"https://jklm.fun/{game_code}")

search = driver.find_element_by_xpath("//input[@class='styled nickname']")
time.sleep(1)

#Player name
player_name = 'Marcel'
search.send_keys(player_name)
search.send_keys(Keys.RETURN)
time.sleep(3)

wait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it(driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/iframe")))

driver.find_element_by_css_selector('button.joinRound').click()

status = driver.find_element_by_css_selector('header.status')


while status.text == '⏳ En attente de 1 autres joueurs…' or status.text == '⏳ En attente de 2 autres joueurs…':
    time.sleep(3)
    continue

# While la partie a commencé
while True:
    if driver.find_element_by_css_selector('div.syllable').text != '':
        syllables = driver.find_element_by_css_selector('div.syllable').text
        break


alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H','I','J','L','M','N','O','P','Q','R','S','T','U','V']
alphabet_marcel = alphabet.copy()
while True:
    time.sleep(1)
    isBotTurn = (driver.find_element_by_css_selector('span.player').text == '')
    if isBotTurn:
        syllables = driver.find_element_by_css_selector('div.syllable').text
        if len(alphabet_marcel) == 0:
            alphabet_marcel = alphabet.copy()
        # Trouver le mot dans le dico: 
        for word in dico:
            if syllables in word:
                if alphabet_marcel[0] in word:
                    for letter in word:
                        if letter in alphabet_marcel:
                            alphabet_marcel.remove(letter)
                    word_play = word
                    break
            
        answer = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[2]/div[2]/form/input")
        if answer:
            answer.send_keys(word_play)
            time.sleep(1)
            answer.send_keys(Keys.RETURN)
            
            dico.remove(word_play)
    continue
    
    #dico.pop(word)
    #Enlever mot du dico



