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

#Stores old directory and changes current
first_directory = os.getcwd()
change_directory('/Database/')

#Headings
boxscore_head = ['Year', 'Week', 'Home', 'Home Score', 'Away', 'Away Score', 'ID']
win_head = ['Year', 'Team', 'Win Total', 'Actual Wins']

#Create lists of database
boxscore_list = database_reader('Boxscore-Database.csv', boxscore_head)
win_list = database_reader('Win-Total-Database.csv', win_head)

head = ['Year','Team','Wins']
os.chdir(first_directory)
change_directory('/Model/')
database('PS-Win-Total-Model', head)  

for year in range(2012, 2020):
    teams = []
    w_teams = []

    for win_total in win_list:
        stats = [year]

        #Pulls last years wins
        if int(win_total[0]) == year - 1:
            stats.append(win_total[1])
            stats.append(float(win_total[3]))
            teams.append(stats)

        #Pulls this years win total
        elif int(win_total[0]) == year:
            for team in teams:
                if team[1] == win_total[1]:
                    team[2] = float(win_total[2])- float(team[2])
                    w_teams.append(team)

    teams = []
    index = 0


    for team in w_teams:
        if 'St Louis Rams' == team[1]:
            team[1] = 'St. Louis Rams'
        fp = 0
        ap = 0
        #Finds season points for and against
        for points in boxscore_list:
            if int(points[0]) == year - 1:
                if team[1] == points[2]:
                    fp += float(points[3])
                    ap += float(points[5])
                elif team[1] == points[4]:
                    fp += float(points[5])
                    ap += float(points[3])
                    
        #Pythagorean Expectation Formula
        pyth = (fp**2.37/(fp**2.37+ap**2.37)) *16
        w_teams[index][2] = w_teams[index][2] + pyth
        index += 1

    for row in w_teams:
        database('PS-Win-Total-Model', row)                
            





