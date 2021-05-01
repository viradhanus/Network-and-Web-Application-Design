import requests
import json

url = 'https://api.github.com/user/repos'

with requests.Session() as session:

    session.headers['Authorization'] = 'token '

    data = json.dumps({'name':'test', 'description':'some test repo'})
    response = session.post(url,data)

print(response.headers)
print("")
print(response.json())
