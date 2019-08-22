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

game_data = ['Year', 'Week', 'Home', 'Away', 'Spread', 'Total']
vi_list = []
database('Spread-Database', game_data)

#beautifulsoup4 link
for year in range(2010,2020):
    for week in range(1,18):
        BS_link = 'http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/' + str(week) + '/season/' + str(year)
        sauce = requests.get(BS_link)
        soup = bs4.BeautifulSoup(sauce.text, 'html.parser')
        for player in soup.find_all('td', {"class":["viCellBg2 cellBorderL1 cellTextNorm padCenter", "viHeaderNorm"]}):

            #Splits needed information
            gdata = (player.text)
            gdata = re.split('>|<', gdata)
            gdata = gdata[0].strip()

            #Checks For Home and Away Teams
            if len(gdata) > 5: 
                gdata = re.split(' @ ', gdata)
                game_data[2] = gdata[1]
                game_data[3] = gdata[0]
                vi_list = []
                index = 0
                max_len = 100

            #Adds stats to temp list
            else:
                vi_list.append(gdata)
                index += 1

            #Check length of temp list
            if index == 5:
                if '%' in vi_list[4]:
                    max_len = 10
                else:
                    max_len = 8

            #Writes Spread and Total to Game list
            if len(vi_list) == max_len:
                if '-' in vi_list[1]:
                    game_data[4] = vi_list[1][1:]
                elif vi_list[1] == 'PK':
                    game_data[4] = '0'
                elif '-' not in gdata:
                    game_data[5] = vi_list[1]

                #Long List
                if max_len == 10:
                    if '-' in vi_list[6]:
                        game_data[4] = vi_list[6]
                    elif vi_list[6] == 'PK':
                        game_data[4] = '0'
                    elif '-' not in gdata:
                        game_data[5] = vi_list[6]

                #Short List
                elif max_len == 8:
                    if '-' in vi_list[5]:
                        game_data[4] = vi_list[5]
                    elif vi_list[5] == 'PK':
                        game_data[4] = '0'
                    elif '-' not in gdata:
                        game_data[5] = vi_list[5]

                #Writes list to CSV file
                game_data[0] = year
                game_data[1] = week
                database('Spread-Database', game_data)
                game_data = ['','','','','','']

