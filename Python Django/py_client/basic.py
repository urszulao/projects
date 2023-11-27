import requests

#endpoint = "https://httpbin.org/status/200/"
#endpoint = "https://httpbin.org/anything"
endpoint =  "http://localhost:8000/api/"  #http://127.0.0.1:8000/

get_response = requests.get(endpoint,  json={"query": "Hello World"})    # API  -> Method Ap ication Programming Interface  / REST APIs -> Web API (using HTTP request) / HTTP Request
#print(get_response.text)                 # print raw  text response   | http request -> html / rest api  http request -> JSON(xml) | JavaScript Object Notation ~ Python Dict

print(get_response.json())    
#print(get_response.status_code)

