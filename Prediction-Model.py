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
 
#Headings
spread_head = ['Year', 'Week', 'Home', 'Away', 'Spread', 'Total']
win_head = ['Year', 'Team', 'Wins']

#Create lists of database
change_directory('/Database/')
spread_list = database_reader('Spread-Database.csv', spread_head)
os.chdir(first_directory)
change_directory('/Model/')
win_list = database_reader('PS-Win-Total-Model.csv', win_head)


head = ['Year','Week','Matchup','Spread','Away Wins','Home Wins','Advantage','ADV Team']
#database('Prediction-Model', head)  

for year in range(2019, 2020):
    for week in range(1, 2):
        for game in spread_list:
            if game[0] == str(year) and game[1] == str(week):
                home_score = 0
                away_score = 0
                for team in win_list:
                    if team[0] == str(year):
                        if team[1] == game[2]:
                            home_score = team[2]
                        elif team[1] == game[3]:
                            away_score = team[2]
                adj_spread = ((float(away_score) - float(home_score))*2)-3
                advantage = float(game[4]) - adj_spread
                head = [year,week,game[3] + ' @ ' + game[2],game[4],away_score,home_score,advantage,'-']
                if advantage < 0:
                    head[7] = game[3]
                elif advantage > 0:
                    head[7] = game[2]
                #database('Prediction-Model', head)
