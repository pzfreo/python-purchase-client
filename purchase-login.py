import requests
import os
import webbrowser
import time
import yaml
from pathlib import Path

client_id = 'purchase';
client_secret = os.environ['CLIENT_SECRET']
oauth_host = os.environ['OAUTH2_HOST']
oauth_port = os.environ['OAUTH2_PORT']

base_url = 'http://'+oauth_host+':'+oauth_port
device_url = '/realms/purchase/protocol/openid-connect/auth/device'
token_url = '/realms/purchase/protocol/openid-connect/token'


r = requests.post(base_url+device_url, data = {'client_id':client_id}, auth=(client_id, client_secret))

resp = r.json()
webbrowser.open_new(resp['verification_uri_complete']);

access_token = "";
refresh_token = "";

finished = False

reqdata = {
    'grant_type': "urn:ietf:params:oauth:grant-type:device_code",
    'device_code': resp['device_code'],
    'client_id': client_id
}

while not finished:
    r = requests.post(base_url+token_url, data = reqdata, auth=(client_id, client_secret))
    if (r.status_code==200):
        tokendata = r.json()
        access_token = tokendata['access_token']
        refresh_token = tokendata['refresh_token']
        finished = True
        break
    time.sleep(resp['interval'])

config = {
    'access_token': access_token,
    'refresh_token': refresh_token
}



home = str(Path.home())

Path(home + "/.config/purchase").mkdir(parents=True, exist_ok=True)
with open(home + '/.config/purchase/secrets', 'w') as file:
    documents = yaml.dump(config, file)





