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

spread_fix = [['2016','1','Denver Broncos','Carolina Panthers','3','40.5'],['2016','1','Atlanta Falcons','Tampa Bay Buccaneers','-2.5','47'],['2016','1','Tennessee Titans','Minnesota Vikings','2.5','40'],['2016','1','Philadelphia Eagles','Cleveland Browns','-3.5','41'],['2016','1','New York Jets','Cincinnati Bengals','1','42'],['2016','1','New Orleans Saints','Oakland Raiders','-3','50.5'],['2016','1','Kansas City Chiefs','Los Angeles Chargers','-6.5','46'],['2016','1','Baltimore Ravens','Buffalo Bills','-3','44.5'],['2016','1','Houston Texans','Chicago Bears','-5.5','42.5'],['2016','1','Jacksonville Jaguars','Green Bay Packers','3.5','47.5'],['2016','1','Seattle Seahawks','Miami Dolphins','-10.5','44'],['2016','1','Dallas Cowboys','New York Giants','1','47.5'],['2016','1','Indianapolis Colts','Detroit Lions','-2.5','51.5'],['2016','1','Arizona Cardinals','New England Patriots','-8.5','44'],['2016','1','Washington Redskins','Pittsburgh Steelers','2.5','49'],['2016','1','San Francisco 49ers','Los Angeles Rams','2.5','43.5'],['2018','3','Washington Redskins','Green Bay Packers','2.5','46'],['2018','3','Minnesota Vikings','Buffalo Bills','-17','41'],['2018','3','Kansas City Chiefs','San Francisco 49ers','-6','53.5'],['2018','3','Los Angeles Rams','Los Angeles Chargers','-7','49'],['2018','3','Arizona Cardinals','Chicago Bears','5.5','39']]

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

                #Write Year and Week
                game_data[0] = year
                game_data[1] = week

                #Fix for broken games
                if '2016' == str(year) and '1' == str(week) or '2018' == str(year) and '3' == str(week):
                    for fix in spread_fix:
                        if fix[2] == game_data[2] and fix[0] == str(year) and fix[1] == str(week):
                            game_data = fix

                if game_data[2] == 'San Diego Chargers':
                    game_data[2] = 'Los Angeles Chargers'
                if game_data[3] == 'San Diego Chargers':
                    game_data[3] = 'Los Angeles Chargers'
                if game_data[2] == 'St. Louis Rams':
                    game_data[2] = 'Los Angeles Rams'
                if game_data[3] == 'St. Louis Rams':
                    game_data[3] = 'Los Angeles Rams' 
                
                #Writes list to CSV file
                database('Spread-Database', game_data)
                game_data = ['','','','','','']

