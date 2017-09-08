import datetime
import pytz
import json
import messenger
import base64
import requests

def convertdate():
    date = datetime.datetime.now(pytz.timezone('US/Eastern'))
    if(date.day<10):
        day = "0{}".format(date.day)
    else:
        day = date.day

    if(date.month<10):
        month = "0{}".format(date.month)
    else:
        month = date.month
    
    est = ("{}{}{}".format(date.year,month,day))
    return(est)


def getdata():
    # Request
    now = datetime.datetime.now()
    if(now.day<10):
        day = "0{}".format(now.day)
    else:
        day = now.day
    
    if(now.month<10):
        month = "0{}".format(now.month)
    else:
        month = now.month
    
    date = "{}{}{}".format(now.year, month, day)

    url = "https://www.mysportsfeeds.com/api/feed/pull/nba/current/daily_game_schedule.json"

    querystring = {"fordate":"{}".format(date)}

    headers = {"authorization": "Basic YmJ1cmtlOTU6YnJlbmRhbjEyMw=="}

    response = requests.request("GET", url, headers=headers, params=querystring)

    return(response.text)


def getboxscore():

    url = "https://www.mysportsfeeds.com/api/feed/pull/nba/2016-2017-regular/scoreboard.json"
    querystring = {"fordate":"{}".format(convertdate())}
    
    headers = {"authorization": "Basic YmJ1cmtlOTU6YnJlbmRhbjEyMw=="}
    
    response = requests.request("GET", url, headers=headers, params=querystring) 
    return(response.text)



def getgames():
    data = getdata()
    jsonObject = json.loads(data)
    counter = 1
    msg = "Respond with the game numbers you would like to follow for today.\n \n";
    index = 0;
    for i in jsonObject["dailygameschedule"]["gameentry"]:      
        tipoff = i["time"]+ " EST"
        msg += "{}) {} {} vs {} {} at {}\n".format(counter,
                i["homeTeam"]["City"],
                i["homeTeam"]["Name"],
                i["awayTeam"]["City"], 
                i["awayTeam"]["Name"],
                tipoff)
        counter += 1
        index += 1
    print(msg)
    messenger.sendDailyNBAGames(msg)

def getscores():
    scoredict = {}
    box = json.loads(getboxscore())
    gamescores = box["scoreboard"]["gameScore"]
    for i in range(len(gamescores)):
        if (gamescores[i]["isUnplayed"] == "false") & (gamescores[i]["isInProgress"] == "false"):
            scoredict[i+1] = "{} {} - {} {} \n \n".format(gamescores[i]["game"]["homeTeam"]["Abbreviation"], 
                gamescores[i]["homeScore"], 
                gamescores[i]["game"]["awayTeam"]["Abbreviation"], 
                gamescores[i]["awayScore"])

    return(scoredict)

def sendUsersMessage():
    getgames()

#sendUsersMessage()
#print(getscores())
