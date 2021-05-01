from urllib import request
from typing import List
import json
import requests


def spider_metadata(urls: List[str]) -> List[List]:
    lh = []     # list to hold headers
    for i in urls:
        #answer for the last one
        h = requests.head(i,data = {'key':'value'}).headers
        lh.append(list(h.items()))

        # response = request.urlopen(i)
        # lh.append(response.headers.items())

    return lh


print(spider_metadata({"http://www.pdn.ac.lk","http://www.google.com"}))

        

    
        
    
    
