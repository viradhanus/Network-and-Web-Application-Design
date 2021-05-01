import requests

response = requests.get('https://api.github.com/viradhanus')

print(response.headers)
print("")
print(response.json())
