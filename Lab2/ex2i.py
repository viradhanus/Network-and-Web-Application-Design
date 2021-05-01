from urllib import parse, request

url_name =  parse.quote("විරාජ් ධනුෂ්ක")

final_url = "https://www.duckduckgo.com/?q=" + url_name + "&format=json&pretty=1"

with request.urlopen(final_url) as query:

    headers = query.headers.items()
    body = query.read()
    print(body.decode("utf-8"))
