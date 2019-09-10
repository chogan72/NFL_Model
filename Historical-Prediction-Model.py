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

def database_reader(current_file, head_list):
    #Read Database Files
    database_players = []
    with open(current_file) as csvfile:
        reader = csv.DictReader(csvfile)
        #Reads rows of CSV file
        for row in reader:
            index = 0
            player_list = []
            #Sets row to proper information
            while index < len(row):
                player_list.append(row[head_list[index]])
                index += 1
            database_players.append(player_list)
    return(database_players)

#Stores old directory
first_directory = os.getcwd()

for mult in range(1,52,5):
    mult = mult / 1000
    os.chdir(first_directory)
    #Headings
    spread_head = ['Year', 'Week', 'Home', 'Away', 'Spread', 'Total']
    win_head = ['Year','Week', 'Team', 'Wins']

    #Create lists of database
    change_directory('/Database/')
    spread_list = database_reader('Spread-Database.csv', spread_head)
    os.chdir(first_directory)
    change_directory('/Historical-Test/')
    win_list = database_reader('Weekly-Win-Total-Model-' + str(mult)[2:] + '.csv', win_head)


    head = ['Year','Week','Home','Spread','Home Wins','Away','Away Wins','Advantage','ADV Team']
    database('Prediction-Model-' + str(mult)[2:], head)  

    for year in range(2011, 2019):
        for week in range(1, 18):
            for game in spread_list:
                if game[0] == str(year) and game[1] == str(week):
                    home_score = 0
                    away_score = 0
                    for team in win_list:
                        if team[0] == str(year) and team[1] == str(week):
                            if team[2] == game[2]:
                                home_score = team[3]
                            elif team[2] == game[3]:
                                away_score = team[3]
                    adj_spread = ((float(away_score) - float(home_score))*2)-3
                    advantage = float(game[4]) - adj_spread
                    head = [year,week,game[2],game[4],home_score,game[3],away_score,advantage,'-']
                    if advantage < 0:
                        head[8] = game[3]
                    elif advantage > 0:
                        head[8] = game[2]
                    database('Prediction-Model-' + str(mult)[2:], head)

