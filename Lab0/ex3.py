#!/usr/bin/python

def load_users_to_dict(filename):

    users = dict()

    with open(filename) as f:

        for line in f:

            id, login = line.split()

            # add details to the users dict
            users[id] = login

    return users


# e.How do you look up a user’s login given their id?

users = load_users_to_dict("userdata.txt")
print(users["112"])

# f.Suppose you want to do the opposite. That is, look up the id of a user when given their login. How would you modify this function?

# Consider the function load_users_from_logins

def load_users_to_dict(filename, name):

    users = dict()

    with open(filename) as f:

        for line in f:

            id, login = line.split()

            # add details to the users dict
            users[id] = login

    user_ids = list()
    for x in users:
        if users[x] == name:  
            user_ids.append(x)
    return user_ids

#Then we can call the function to get the answer.
print(load_users_to_dict("userdata.txt", "samanthi"))

# g.Suppose the data file format is modified to store the id and login separated by a comma(,) Modify this function to handle the change.

def load_users_to_dict_from_csv(filename):
    users = dict()

    with open(filename) as f:

        for line in f:

            id, login = line.split(",")

            # add details to the users dict
            users[id] = login

    return users

#let's call the function
users_from_csv = load_users_to_dict_from_csv("userdata_csv.txt")
print(users_from_csv["112"])