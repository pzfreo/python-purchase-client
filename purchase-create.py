import os.path
from pathlib import Path

import yaml
import requests

home = str(Path.home())


if not os.path.isfile(home+"/.config/purchase/secrets"):
    print ("secrets file is not present, login first")    
    exit


bearer = ""
refresh = ""

with open(home + '/.config/purchase/secrets') as file:
    secrets = yaml.load(file, Loader=yaml.FullLoader)
    bearer = secrets['access_token']
    refresh = secrets['refresh_token'] 


purchase_url = 'http://localhost:8000/purchase'

data = {
    'paymentReference': "PR0001",
    'poNumber': "PON0001",
    'quantity': 3,
    'customerNumber': "CUS0001",
    'lineItem': "LI0001"
}

headers = {
  'Authorization': 'Bearer '+bearer
}

response = requests.post(purchase_url, headers=headers, json=data)

print(response.text)