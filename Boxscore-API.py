from sportsreference.nfl.boxscore import Boxscores
import os
import csv


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

#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')

game_list = ['Year', 'Week', 'Home', 'Home Score', 'Away', 'Away Score', 'ID']
database('Boxscore-Database', game_list)

for year in range(2010, 2020):
    for week in range(1, 18):
        game_list[0] = year
        game_list[1] = week
        games = Boxscores(week, year)
        for f_key, f_value in games.games.items():
            for current_dict in f_value:
                for s_key, s_value in current_dict.items():
                    if s_key == 'boxscore':
                        game_list[6] = s_value
                    elif s_key == 'home_name':
                        game_list[2] = s_value
                    elif s_key == 'home_score':
                        game_list[3] = s_value
                    elif s_key == 'away_name':
                        game_list[4] = s_value
                    elif s_key == 'away_score':
                        game_list[5] = s_value
                database('Boxscore-Database', game_list)
