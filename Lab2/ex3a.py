from urllib import request
from typing import List
import json

def ddg_query(url: str, nr_results: int) -> List[str]:
    
    #create 3 list type variables

    words = []      #list to hold words   
    results = []    #list to hold results
    T_list = []     #list to hold topics

    
    words = url.strip().split()
    url_name = "+".join(words)
    
    #get the final url by concatinating with DDG
    final_url = "https://www.duckduckgo.com/?q=" + url_name + "&format=json&pretty=1"
    
    
    with request.urlopen(final_url) as query:
        
        body = query.read().decode("utf-8")
        json_body = json.loads(body)

        for result in json_body['Results']:
            results.append(result['FirstURL'])

        # print(json_body['RelatedTopics'])
        for related_topic in json_body['RelatedTopics']:
            T_list.append(related_topic['FirstURL'])

        URLS = results + T_list
        # print(URLS)
        if (nr_results > len(URLS)):
            return URLS

        return (URLS[:nr_results])



print (ddg_query("University Of Peradeniya",3)) #should return something like [“http://www.pdn.ac.lk/”]



    
        
    
    
