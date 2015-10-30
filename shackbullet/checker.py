import web
import requests
import uuid
import json
import time
from config import *

#get secrets from config file
accesstoken = PB_ACCESS_TOKEN
clientid = PB_CLIENT_ID
clientsecret = PB_CLIENT_SECRET

#get client uuid and pushbullet key from  ???
userpbkey = 'undefined'
wcuuid = 'undefined'

while True:
    #Chloe, open a socket to Winchatty and wait for a notification
    payload = { 'clientId' : wcuuid }
    r = requests.post("http://notifications.winchatty.com/v2/notifications/waitForNotification", data=payload)
    winchattydata = json.loads(r.text)
    for messages in winchattydata['messages']:
        #got a response get the list of devices connected to pushbullet
        pbheaders = {'Access-Token' : userpbkey}
        r = requests.get("https://api.pushbullet.com/v2/devices", headers=pbheaders)
        pbdata = json.loads(r.text)
        for dev in pbdata['devices']:
            #check if it's an iOS device
            if 'type' in dev:
                if 'ios' in dev['type']:
                    #it's an iOS device send a push with a latestchatty URI
                    payload = { 'type' : 'link', 'device_iden' : dev['iden'],'title' : messages['subject'] + ': ' + messages['body'], 'body' : messages['body'], 'url' : 'LatestChatty://www.shacknews.com/chatty?id=' + str(messages['postId']) + '#item_' + str(messages['postId']) }
                    r = requests.post("https://api.pushbullet.com/v2/pushes", headers=pbheaders, data=payload)
                else:
                    #has a type, but not iOS send regular http link
                    payload = { 'type' : 'link', 'device_iden' : dev['iden'],'title' : messages['subject'] + ': ' + messages['body'], 'body' : messages['body'], 'url' : 'http://www.shacknews.com/chatty?id=' + str(messages['postId']) + '#item_' + str(messages['postId']) }
                    r = requests.post("https://api.pushbullet.com/v2/pushes", headers=pbheaders, data=payload)
            else:
                #has no type, send http link
                payload = { 'type' : 'link', 'device_iden' : dev['iden'],'title' : messages['subject'] + ': ' + messages['body'], 'body' : messages['body'], 'url' : 'http://www.shacknews.com/chatty?id=' + str(messages['postId']) + '#item_' + str(messages['postId']) }
                r = requests.post("https://api.pushbullet.com/v2/pushes", headers=pbheaders, data=payload)
    time.sleep(3)