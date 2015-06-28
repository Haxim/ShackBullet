#Import the modules
import requests
import json
import uuid

#Edit these to your shacknews login credentials
shackname = 'Username'
shackpass = 'ShackPassword'
pushbulletkey = 'access token from https://www.pushbullet.com/account'

#Fun Begins

#generate uuid from namespace
uuid = uuid.uuid5(uuid.NAMESPACE_DNS, 'winchatty.com')
#setup registration payload
payload = { 'id' : uuid, 'name' : 'shackbullet', 'username' : shackname, 'password' : shackpass }

#register this client
r = requests.post("https://winchatty.com/v2/notifications/registerRichClient", data=payload)

#We are setup so start waiting for notifications
#setup checking payload
payload = { 'clientId' : uuid }
bulletheaders = { 'Authorization' : 'Bearer ' + pushbulletkey }
#main loop to check for notifications
while True:
    #wait for notifications
    r = requests.post("http://notifications.winchatty.com/v2/notifications/waitForNotification", data=payload)
    data = json.loads(r.text)
    #got a response, now iterate over the reponses and send them to pushbullet
    for messages in data['messages']:
        bulletpayload = { 'type' : 'link', 'title' : messages['subject'] + ': ' + messages['body'], 'body' : messages['body'], 'url' : 'LatestChatty://www.shacknews.com/chatty?id=' + str(messages['postId']) + '#item_' + str(messages['postId']) }
        #send the notification to pushbullet
        r = requests.post("https://api.pushbullet.com/v2/pushes", headers=bulletheaders, data=bulletpayload)
