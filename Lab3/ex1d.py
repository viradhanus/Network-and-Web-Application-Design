import requests

with requests.Session() as session:

    session.headers['Authorization'] = 'token 5ffaf0a4fcea7fd13d897967707e390a6947a267'
    response = session.get('https://api.github.com/user')

print(response.headers)
print("")
print(response.json())