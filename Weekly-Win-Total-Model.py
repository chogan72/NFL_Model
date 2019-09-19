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
spread_head = ['Year','Week','Home','Away','Spread','Total']

#Create lists of database
boxscore_list = database_reader('Boxscore-Database.csv', boxscore_head)
win_list = database_reader('Win-Total-Database.csv', win_head)
spread_list = database_reader('Spread-Database.csv', spread_head)

for year in range(2019, 2020):
    head = ['Year','Week','Team','Wins']
    os.chdir(first_directory)
    change_directory('/Model/')
    database(str(year) + '-Weekly-Win-Total-Model', head) 
    teams = []
    w_teams = []
    for week in range (1, 4):
        if week == 1:
            for win_total in win_list:
                stats = [year,week]
                #Pulls last years wins
                if int(win_total[0]) == year - 1:
                    stats.append(win_total[1])
                    stats.append(float(win_total[3]))
                    teams.append(stats)
                #Pulls this years win total
                elif int(win_total[0]) == year:
                    for team in teams:
                        if team[2] == win_total[1]:
                            team[3] = float(win_total[2])- float(team[3])
                            w_teams.append(team)
                
            teams = []
            index = 0

            for team in w_teams:
                fp = 0
                ap = 0
                #Finds season points for and against
                for points in boxscore_list:
                    if int(points[0]) == year - 1:
                        if team[2] == points[2]:
                            fp += float(points[3])
                            ap += float(points[5])
                        elif team[2] == points[4]:
                            fp += float(points[5])
                            ap += float(points[3])
                
                #Pythagorean Expectation Formula
                pyth = (fp**2.37/(fp**2.37+ap**2.37)) *16
                w_teams[index][3] = w_teams[index][3] + pyth
                index += 1

        else:
            for team in w_teams:
                if year == team[0] and team[1] == week -1:
                    new = 0
                    for points in boxscore_list:
                        if str(year) == points[0] and int(points[1]) == week -1 and team[2] == points[2]:
                            new = (float(points[3]) - float(points[5]))
                        elif str(year) == points[0] and int(points[1]) == week -1 and team[2] == points[4]:
                            new = (float(points[5]) - float(points[3]))
                    for spread in spread_list:
                        if str(year) == spread[0] and int(spread[1]) == week -1 and team[2] == spread[2]:
                            new = (new + float(spread[4])) * .01
                        elif str(year) == spread[0] and int(spread[1]) == week -1 and team[2] == spread[3]:
                            new = (new - float(spread[4])) * .01
                    new_list = [year,week,team[2],team[3] +  new]
                    w_teams.append(new_list)

    for row in w_teams:
        database(str(year) + '-Weekly-Win-Total-Model', row)                
