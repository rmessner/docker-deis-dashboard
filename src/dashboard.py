from flask import Flask, render_template, request, Response
from flask import make_response
from flask.ext.triangle import Triangle
import deis as DeisClient
import json

app = Flask(__name__, static_path='/static')
app.debug = True
Triangle(app)

@app.route('/')
def index():
    user = {"username": request.cookies.get("deis_username"),"token": request.cookies.get("deis_token") }
    if user.get("token") != None :
       return render_template('apps.html', user=user)
    else:
       return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = DeisClient.deis_login(request.form['username'], request.form['password'])
        resp = make_response(render_template('apps.html', user=user))
        resp.set_cookie("deis_username", user.get("username"))
        resp.set_cookie("deis_token", user.get("token"))
        return resp
    else:
        return render_template('index.html', error=error)

@app.route('/apps/list')
def apps_list():
    token = request.cookies.get("deis_token") 
    return Response(response=json.dumps(DeisClient.deis_list_apps(token)),status=200, mimetype="application/json")

@app.route('/apps/create/<name>')
def apps_create(name):
    token = request.cookies.get("deis_token") 
    return Response(response=json.dumps(DeisClient.deis_create_app(token, name)),status=200, mimetype="application/json")    
    
@app.route('/apps/<app>/containers/list')
def containers_list(app):
    token = request.cookies.get("deis_token") 
    return Response(response=json.dumps(DeisClient.deis_list_containers(token,app)),status=200, mimetype="application/json")
    
@app.route('/apps/<app>/scale/<int:count>')
def containers_scale(app,count):
    token = request.cookies.get("deis_token") 
    DeisClient.deis_scale(token,app,count)
    return Response(response=json.dumps({}),status=200, mimetype="application/json")
        
@app.route('/apps/<app>/builds/list')
def builds_list(app):
    token = request.cookies.get("deis_token") 
    return Response(response=json.dumps(DeisClient.deis_list_builds(token,app)),status=200, mimetype="application/json")
    
@app.route('/apps/<app>/builds/create', methods=['GET', 'POST'])
def builds_create(app):
    token = request.cookies.get("deis_token")
    image = request.form['image']
    return Response(response=json.dumps(DeisClient.deis_create_build(token,app,image)),status=200, mimetype="application/json")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
