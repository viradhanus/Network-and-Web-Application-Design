import requests
import json
from ex2a import github_superstars

# https://github.com/cepdnaclk
orgnanization = 'cepdnaclk'

repo_superstars_list = github_superstars(orgnanization)

#consider repo superstar as the first one(with most stars) in the list
repo_superstar = repo_superstars_list[0]

print("Repo superstar is :")
print(repo_superstar)
repoUrl = repo_superstar[0]

with requests.Session() as session:
    session.headers['Authorization'] = 'token 5ffaf0a4fcea7fd13d897967707e390a6947a267'

# watch the repo that wins github_superstars
session.put(repoUrl+'/subscription')
