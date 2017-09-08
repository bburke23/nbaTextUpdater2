import app

def sendScores():
    scores = app.sendUsersEndScores()
    print("Finished: ");
    print(str(scores));


sendScores()
