import requests

with requests.Session() as session:

    session.headers['Authorization'] = 'token '
    response = session.get('https://api.github.com/user')

print(response.headers)
print("")
print(response.json())
