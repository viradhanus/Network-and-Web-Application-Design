import requests
import json


from typing import List, Tuple


def github_superstars(orgnanization: str) -> List[Tuple]:

    with requests.Session() as session:
        session.headers['Authorization'] = 'token 5ffaf0a4fcea7fd13d897967707e390a6947a267'

    # 1. Get a list of members in the Github organization

    response_members = session.get('https://api.github.com/orgs/' + orgnanization + '/members')


    members = []    #create a list to hold members
    resp_mem_list = response_members.json() #get the memberlist from response
    # print(resp_mem_list[3])

    for x in resp_mem_list:
        members.append(x['login'])  #append members to the members list
    # print("List of members :")
    # print(members)
    # print("")

    #extract repo names with maximum stars to a list from all members
    all_max_star_repos_extracted_list = []  

    # 2. For each member, find the repo they own with the most stars.

    repos_dict = {} #dictionary to hold repos

    # NOTE: WE COULD HAVE USED  repos_url AS WELL

    for member in members:
        response_repos = session.get('https://api.github.com/users/' + member +'/repos'+"?page=1&per_page=150")
        repos_dict[member] = response_repos.json()

        repo_list = repos_dict[member] #get all the repos of a perticular member
        member_repos_extracted_dict = {}   #extract repo names and stars to a dict for a perticular member
    
        #Instead of repo name, used repo url (2nd question needs that way)
        for repo in repo_list:
            member_repos_extracted_dict[repo['url']] = repo['stargazers_count']    #for 1 member
        
        member_max_star_repos_extracted_list = [(keys,values) for keys,values in member_repos_extracted_dict.items() if values == max(member_repos_extracted_dict.values())]
        # print('Repos of '+ member + ' with the most stars :')
        # print(member_max_star_repos_extracted_list)
        # print("")

        # 3. Add the repo name and the number of stars it has to a list.
        all_max_star_repos_extracted_list.extend(member_max_star_repos_extracted_list) 

    # all repo names with maximum number of stars    
    # print(all_max_star_repos_extracted_list)
    # print("")

    # 4. Return the list sorted in descending order of stars.
    return sorted(all_max_star_repos_extracted_list,key=lambda x: x[1],reverse=True)



# orgnanization = 'cepdnaclk'
# print(github_superstars(orgnanization))