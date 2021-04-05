import requests
import os
import webbrowser
import time
import yaml
from pathlib import Path

client_id = 'purchase'
client_secret = os.environ['CLIENT_SECRET']
oauth_host = os.getenv('OAUTH2_HOST', 'localhost')
oauth_port = os.getenv('OAUTH2_PORT', '8080')

base_url = 'http://'+oauth_host+':'+oauth_port
device_url = '/realms/purchase/protocol/openid-connect/auth/device'
token_url = '/realms/purchase/protocol/openid-connect/token'


#  call the device code api
print("calling device api")

r = requests.post(base_url+device_url, data = {'client_id':client_id}, auth=(client_id, client_secret))

resp = r.json()
print("received response")
print (resp)

# Open the returned URL
print ("opening url", resp['verification_uri_complete'])
webbrowser.open_new(resp['verification_uri_complete']);

access_token = ""
refresh_token = ""

finished = False

reqdata = {
    'grant_type': "urn:ietf:params:oauth:grant-type:device_code",
    'device_code': resp['device_code'],
    'client_id': client_id
}

print ("polling for tokens while user does browser flow")
# Poll for the tokens
while not finished:
    r = requests.post(base_url+token_url, data = reqdata, auth=(client_id, client_secret))
    print("recieved status code", r.status_code)
    if (r.status_code==200):
        tokendata = r.json()
        access_token = tokendata['access_token']
        refresh_token = tokendata['refresh_token']
        finished = True
        break
    print ("waiting")
    time.sleep(resp['interval'])


config = {
    'access_token': access_token,
    'refresh_token': refresh_token
}

print ("saving to ~/.config/purchase/secrets")
print (yaml.dump(config))
# save the tokens to the home directory

home = str(Path.home())

Path(home + "/.config/purchase").mkdir(parents=True, exist_ok=True)
with open(home + '/.config/purchase/secrets', 'w') as file:
    documents = yaml.dump(config, file)





