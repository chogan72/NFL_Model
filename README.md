# NFL Model

This analyse weekly spreads to determine an edge.


## Current Status

As of right now the model is ready to go for the 2019 Season.


## Database Files

* Spread Scraper
  * This is used to scrape http://www.vegasinsider.com/nfl/matchups/matchups.cfm/week/1/season/2019 to find the spreads and totals for each game.
  * It used to find historical spreads as well as ones for the current week
  * This is used to create Database/Spread-Database
* Win Total Scraper
  * This is used to scrape https://www.sportsoddshistory.com/nfl-win/?y=2019&sa=nfl&t=win&o=t to find season win totals and actual wins.
  * This is used to create Database/Win-Total-Database.csv
* Boxscore API
  * This uses the sportsreference api (https://sportsreference.readthedocs.io/en/stable/) to pull team stats by games. 
  * This is used to create the files in Database/Boxscore-Database.csv
  
  
## Models

### Weekly Win Total Model

#### Purpose

* This model ajusts the vegas win total based on Pythagorean Differential and Weekly Point Differential
* This model is loosely based of this article by Adam Chernoff: https://medium.com/@adamchernoff/how-to-create-and-use-nfl-power-ratings-to-beat-the-point-spread-3fa4c3ecdc22

#### Pythagorean Differential

* If it is Week 1 these equations are run

<p align="center"> Pythagorean Expectation = (Points For^2.37 / (Points For^2.37 + Points Against^2.37)) * 16</p>

<p align="center"> Pythagorean Differential = Last Year Wins - Pythagorean Expectation </p>

<p align="center"> Adjusted Win Total = Vegas Win Total - Pythagorean Differential </p>

#### Point Differential

* After every week the win totals are adjusted
* After a win, Margin of Victory * .016 is added to the win total
* After a loss, Margin of Victory * .016 is subtracted from the win total

### Prediction Model

* This is used to find the edge

<p align="center"> Home Adjusted Spread = (Away Adjusted Win Total - Home Adjusted Win Total) * 2 - 3 </p>

<p align="center"> Advantage = Real Spread - Home Adjusted Spread </p>

* If the Advantage is negative take the Away Team
* If the Advantage is positive take the Home Team
* If the Advantage is greater than 5 or less than -5 then it is considered a good bet

## Historical Test

#### Purpose

* Historical Prediction Model and Historical Win Total Model pull data for games between 2010 and 2018

#### Historical Test

* Analysis of past seasons to determine the quality of the models
* Current Margin of Victory multiplyer .016
* Current best bet is over 5
