import sys
sys.path.append(".")

import requests

url = "http://0.0.0.0:5000/get-data-advanced/sql"
params = {
    "API_KEY": "foo",
    "query": "select * from theatres;"
}

r = requests.get(url, params)
print(r.json())
