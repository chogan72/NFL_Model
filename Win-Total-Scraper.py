import bs4
import requests
import re
import csv
import os


def change_directory(folder):
    #Change Databse Directory
    dirpath = os.getcwd()
    dirpath = dirpath + folder
    os.chdir(dirpath)

def database(path, item_list):
    #Writes Players to CSV file
    with open(path + '.csv', 'a', newline='') as file:
        wr = csv.writer(file, dialect='excel')
        wr.writerow(item_list)

change_directory('\\Database\\')

game_data = ['Year', 'Team', 'Win Total', 'Actual Wins']
index = 0
database('Win-Total-Database', game_data)

#beautifulsoup4 link
for year in range(2010,2020):
    game_data[0] = year
    BS_link = 'https://www.sportsoddshistory.com/nfl-win/?y=' + str(year) +'&sa=nfl&t=win&o=t'
    sauce = requests.get(BS_link)
    soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
    for player in soup.find_all('td'):
        
        #Splits needed information
        gdata = (player.text)
        gdata = re.split('>|<', gdata)
        gdata = gdata[0].strip()
        
        if len(gdata) > 8:
            game_data[1] = gdata
            index = 0

        elif index == 1:
            game_data[2] = gdata

        elif index == 5:
            game_data[3] = gdata
            database('Win-Total-Database', game_data)
            game_data = [year, '', '', '']

        index += 1
        

        
