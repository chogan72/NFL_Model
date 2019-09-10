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
change_directory('/Historical-Test/')
final = ['First Year','Last Year','Multiplier','Range','Wins','Loses','Push','W%']
database('Final-Test', final)

for mult in range(1,52,5):
    os.chdir(first_directory)
    mult = mult / 1000
    
    #Headings
    prediction_head = ['Year','Week','Home','Spread','Home Wins','Away','Away Wins','Advantage','ADV Team']
    boxscore_head = ['Year', 'Week', 'Home', 'Home Score', 'Away', 'Away Score', 'ID']

    #Create lists of database
    change_directory('/Database/')
    boxscore_list = database_reader('Boxscore-Database.csv', boxscore_head)
    os.chdir(first_directory)
    change_directory('/Historical-Test/')
    prediction_list = database_reader('Prediction-Model-' + str(mult)[2:] +'.csv', prediction_head)

    head = ['Year','Week','Home','Spread','Home Wins','Away','Away Wins','Advantage','ADV Team']
    #database('Prediction-Model', head)  

    for year in range(2011,2019):
        for adv in range(5,6):
            ats_w = 0
            ats_l = 0
            ats_p = 0

            for game in prediction_list:
                final_score = 0
                for score in boxscore_list:
                    if game[0] == score[0] and game[1] == score[1] and game[2] == score[2] and int(game[0]) >= year:
                        final_score = (float(score[3]) + float(game[3])) - float(score[5])
                        if float(game[7]) > adv or float(game[7]) < -adv:
                            if float(final_score) > 0:
                                if game[2] == game[8]:
                                    ats_w +=1
                                else:
                                    ats_l +=1
                            elif float(final_score) < 0:
                                if game[5] == game[8]:
                                    ats_w +=1
                                else:
                                    ats_l +=1
                            elif float(final_score) == 0:
                                ats_p += 1
                                
            if ats_w + ats_l != 0:
                final = [year,2018,mult,adv,ats_w,ats_l,ats_p,(ats_w / (ats_w + ats_l)) * 100]
                database('Final-Test', final)
