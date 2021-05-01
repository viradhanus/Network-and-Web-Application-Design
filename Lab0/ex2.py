#!/usr/bin/python
from ex1 import load_users_to_lists

ids, logins = load_users_to_lists("userdata.txt")
combined = zip(ids, logins)
combined_reversed = zip(logins, ids)

print(combined)
print(combined_reversed)
