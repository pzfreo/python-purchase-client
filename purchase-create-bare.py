import os.path
from pathlib import Path

import requests

home = str(Path.home())


purchase_url = 'http://localhost:8000/purchase'

data = {
    'paymentReference': "PR0001",
    'poNumber': "PON0001",
    'quantity': 3,
    'customerNumber': "CUS0001",
    'lineItem': "LI0001"
}

response = requests.post(purchase_url, json=data)

print(response.text)