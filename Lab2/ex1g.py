from urllib import request

# 1.g
response_g = request.urlopen("https://ta.wikipedia.org/wiki/%E0%AE%9A%E0%AE%BF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AE%AE%E0%AF%8D")
body_g = response_g.read()
print(body_g)


# import requests

# x = requests.get('https://github.com/viradhanus')

# print(x.headers['X-Random'])