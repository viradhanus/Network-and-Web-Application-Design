from urllib import request

# 1.h
response_g = request.urlopen("https://ta.wikipedia.org/wiki/%E0%AE%9A%E0%AE%BF%E0%AE%99%E0%AF%8D%E0%AE%95%E0%AE%B3%E0%AE%AE%E0%AF%8D")
body_g = response_g.read()
print(body_g)
print(" ")
print(" ")
body_h = body_g.decode("utf-8")
print(body_h)