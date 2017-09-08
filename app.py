from flask import Flask, request
import messenger
import os
import psycopg2
import urlparse
import dj_database_url
import sportsradar
import requests

ACCESS_TOKEN = "EAAP9MMaGh1cBAHS7jZCnuQgm2GWx5grLraIElFlWlIw2r3Afb34m2c2rP0xdkkkKEeiBOykGINAP0tScwmL5NNBJQN9ayPCuq13syvWocmbYZA7BXL86FsZCyZBxTmkgYYp8MDulLc1Tx70FGdU5ebQZAJV28nMkZD"

DATABASES = {'default': ""}

DATABASES['default'] =  dj_database_url.config()

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
    return "NBA Updater"

@app.route("/smsresponse", methods=['GET', 'POST'])
def smsresponse():
    num = request.values.get('From', None)
    message = request.values.get('Body', None)
    options = message.split()
    print(options)

    callers = messenger.getContactsSaved()
    if num in messenger.getContactsSaved():
        message = callers[num] + ", thanks for the message!"
    else:
        message = "Thanks for the message!"

    message += " You will be receiving box scores of the specified games."
    
    qry = "UPDATE userselections SET "
    size = len(options)
    count = 1;
    for option in options:
        if(size != count):
            qry+= "\"{}\"=1, ".format(option)
        else:
            qry+= "\"{}\"=1 ".format(option) 
        count+=1

    qry += "WHERE phone = '{}'".format(num)
    cur = conn.cursor()

    cur.execute(qry)
    conn.commit()
    messenger.sendMessage(message, num)
    print(qry);
    return "Messaging Response"


@app.route("/clearTable", methods=['GET', 'POST'])
def clearTable():
    qry = "UPDATE userselections SET"
    for i in range(1, 16):
        if(i != 15):
            qry+= "\"{}\"=0, ".format(i)
        else:
            qry+= "\"{}\"=0 ".format(i)
    cur = conn.cursor()

    cur.execute(qry)
    conn.commit()
    print("Finished clearing table!")

def clearTableOnGameSent(columns, phone):
    qry = "UPDATE userselections SET"
    count = 1;
    for i in range(len(columns)):
        if(count != len(columns)):
            qry+= "\"{}\"=0, ".format(columns[i])
        else:
            qry+= "\"{}\"=0 ".format(columns[i])
        count +=1

    qry += "Where phone = '{}'".format(phone)
    cur = conn.cursor()
    cur.execute(qry)
    conn.commit()


@app.route("/sendEndScores", methods=['GET'])
def sendUsersEndScores():
    scores = sportsradar.getscores()
    print(str(scores))
    if not scores:
        return("No scores yet!")
    cur = conn.cursor()
    cur.execute("""SELECT * FROM userselections""")
    rows = cur.fetchall()

    for row in rows:
        msg = ""
        colsToClear = []
        for i in range(16):
            boolean = row[i]
            if(boolean == 1 and i in scores.keys()):
                msg += scores[i] + "\n"
                colsToClear.append(i);
        if(len(colsToClear) > 0):
           clearTableOnGameSent(colsToClear, row[0])
           if(msg != ""):
               messenger.sendMessage(msg, row)
    return(str(scores))

@app.route('/facebookBot', methods=['POST', 'GET'])
def handle_incoming_messages():
    data = request.json
    if(data is not None):
        sender = data['entry'][0]['messaging'][0]['sender']['id']
        message = "hi"
        reply(sender, message[::-1])
    #return(data['hub.challenge'])
    return request.args.get('hub.challenge')

def reply(user_id, msg):
        data = { "recipient": {"id": user_id},
                 "message": {"text": msg}
                                    }
        resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, 
                json=data)
        print(resp.content)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
