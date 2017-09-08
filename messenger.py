from twilio.rest import TwilioRestClient

account_sid = "AC09524c4f7fa5c5dd8dd27c1c6056e285" # Your Account SID from www.twilio.com/console
auth_token  = "09171df3eeda8c01ea5fc57a0c86ca40"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

def sendDailyNBAGames(msg):
    print("Sending message...");
    for number, contact in getContactsSaved().items():
        message = client.messages.create(body=msg, to=number, from_="+14156530755")

def getContactsSaved():
    contacts = { 
            "+18025352396": "BrenBren",
            "+17075707115": "Jordan"
            }
    return contacts

def sendMessage(msg, num):
    if(num != None):
        message = client.messages.create(body=msg, 
                to=num, 
                from_="+14156530755") # Replace with your Twilio number

#sendDailyNBAGames()

#getContactsSaved()
