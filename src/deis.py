import requests
import json

deis_controller = "http://deis.23.251.142.211.xip.io"

def deis_login(username, password):
    url = deis_controller + "/v1/auth/login/"
    data = { "username": username, "password": password }
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return {"username": username, "token": r.json().get("token")}

def deis_list_apps(token):
    url = deis_controller + "/v1/apps"
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    r = requests.get(url, headers=headers)
    return r.json().get("results")    

def deis_list_builds(token, app):
    url = deis_controller + "/v1/apps/" + app + "/builds"
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    print "Request to deis :" + url
    r = requests.get(url, headers=headers)
    print "<== " + json.dumps(r.json())
    return r.json().get("results")    
    
def deis_list_containers(token, app):
    url = deis_controller + "/v1/apps/" + app + "/containers"
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    r = requests.get(url, headers=headers)
    return r.json().get("results")    

def deis_list_config(token, app):
    url = deis_controller + "/v1/apps/" + app + "/containers"
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    r = requests.get(url, headers=headers)
    return r.json()

def deis_create_app(token, name):
    url = deis_controller + "/v1/apps"
    data = { "id": name }
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.json()

def deis_create_build(token, app, image): 
    url = deis_controller + "/v1/apps/" + app + "/builds"
    data = { "image": image }
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    print "Request to deis :" + url
    print "==> " + json.dumps(data)
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print "<== " + json.dumps(r.json())
    return r.json()

def deis_scale(token, app, count):     
    url = deis_controller + "/v1/apps/" + app + "/scale"
    data = { "cmd": count }
    headers = {'Content-type': 'application/json', 'Authorization': 'token '+ token }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return deis_list_containers(token,app)
