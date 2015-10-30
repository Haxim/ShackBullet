import web
import requests
import uuid
from config import PB_CLIENT_ID

urls = (
  '/shack', 'Shack'
)

app = web.application(urls, globals())

render = web.template.render('templates/')

class Shack(object):
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
        pbredirect_uri = 'http://localhost:8080/shack?uuid=' + str(winchattyuuid.hex)
        return render.pushbullet_form( pbclient_id = pbclient_id, pbredirect_uri = pbredirect_uri )
		
if __name__ == "__main__":
    app.run()