import web
import requests
import uuid
from config import *

accesstoken = PB_ACCESS_TOKEN
clientid = PB_CLIENT_ID
clientsecret = PB_CLIENT_SECRET

urls = (
  '/', 'index'
  '/auth_complete' , 'auth_complete'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class index(object):
    def GET(self):
        return render.shack_form()

    def POST(self):
#Login to shack, if auth is good, register a new rich notification client with winchatty api using those same credentials
        form = web.input()
        shackusername = form.username
        payload = {'username': form.username, 'password': form.password}
        r = requests.post('https://www.winchatty.com/v2/verifyCredentials', data=payload)
        namespace = shackusername + '.winchatty.com'
        namespace = namespace.encode('utf-8')
        winchattyuuid = uuid.uuid5(uuid.NAMESPACE_DNS, namespace)
        payload = { 'id' : uuid, 'name' : 'Shackbullet', 'username' : form.username, 'password' : form.password }
        r = requests.post("https://winchatty.com/v2/notifications/registerRichClient", data=payload)
#If notification client was successful, display a button(?) to link pushbullet account to shackbullet
        pbclient_id = PB_CLIENT_ID
        pbredirect_uri = 'http://localhost:8080/auth_complete?uuid=' + str(winchattyuuid.hex)
        return render.pushbullet_form( pbclient_id = pbclient_id, pbredirect_uri = pbredirect_uri )

class auth_complete(object):
    def GET(self):
        user_data = web.input()
        uuid = user_data.uuid
        pbcode = user_data.code
        #get client access token from code
		headers = { 'Access-Token' : accesstoken }
		payload = { 'client_id' : clientid, 'client_secret' = clientsecret, 'code' = pbcode, 'grant_type' = 'authorization_code' }
		r = requests.post('https://api.pushbullet.com/oauth2/token', headers=headers, data=payload)
		codedata = json.loads(r.text)
		clientpbkey = codedata['access_token']
		#save this key and the winchattyUUID somewhere for use with checker.py

if __name__ == "__main__":
    app.run()